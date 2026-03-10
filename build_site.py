#!/usr/bin/env python3
"""Convert AI architecture lecture markdown into a multi-page HTML site."""

import re
import html

MD_PATH = "/home/claude/ai_system_architecture_lecture.md"
OUT_DIR = "/home/claude/site"

# Chapter definitions: (slug, title, start_marker, end_marker)
CHAPTERS = [
    ("index", "はじめに", "## はじめに", "## 第1章"),
    ("chapter1", "第1章 ステートレス性", "## 第1章", "## 第2章"),
    ("chapter2", "第2章 確率的制御と決定論的制御", "## 第2章", "## 第3章"),
    ("chapter3", "第3章 Harness と Context Engineering", "## 第3章", "## 第4章"),
    ("chapter4", "第4章 AIシステム基盤構造図", "## 第4章", "## 第5章"),
    ("chapter5", "第5章 実践への示唆", "## 第5章", "## 第6章"),
    ("chapter6", "第6章 Harnessの実装", "## 第6章", "## おわりに"),
    ("conclusion", "おわりに・用語集・参考文献", "## おわりに", None),
]

NAV_ITEMS = [
    ("index.html", "はじめに"),
    ("chapter1.html", "第1章"),
    ("chapter2.html", "第2章"),
    ("chapter3.html", "第3章"),
    ("chapter4.html", "第4章"),
    ("chapter5.html", "第5章"),
    ("chapter6.html", "第6章"),
    ("conclusion.html", "おわりに"),
]

def read_md():
    with open(MD_PATH, "r") as f:
        return f.read()

def extract_section(text, start, end):
    si = text.find(start)
    if si == -1:
        return ""
    if end:
        ei = text.find(end, si + len(start))
        if ei == -1:
            return text[si:]
        return text[si:ei]
    return text[si:]

def md_to_html_content(md_text):
    """Simple markdown to HTML converter for our specific content."""
    lines = md_text.split("\n")
    result = []
    in_code = False
    in_table = False
    in_list = False
    code_block = []
    table_rows = []
    
    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                result.append(f'<pre><code>{html.escape(chr(10).join(code_block))}</code></pre>')
                code_block = []
                in_code = False
            else:
                if in_list:
                    result.append("</ul>")
                    in_list = False
                in_code = True
            continue
        
        if in_code:
            code_block.append(line)
            continue
        
        # Tables
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            if line.strip().replace("|", "").replace("-", "").replace(" ", "") == "":
                continue  # separator row
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cols)
            continue
        elif in_table:
            # End table
            result.append('<div class="table-wrap"><table>')
            for i, row in enumerate(table_rows):
                tag = "th" if i == 0 else "td"
                result.append("<tr>" + "".join(f"<{tag}>{format_inline(c)}</{tag}>" for c in row) + "</tr>")
            result.append("</table></div>")
            in_table = False
            table_rows = []
        
        # Empty line
        if line.strip() == "":
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append("")
            continue
        
        # Headers
        if line.startswith("### "):
            if in_list:
                result.append("</ul>")
                in_list = False
            text = line[4:].strip()
            anchor = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-').lower()
            result.append(f'<h3 id="{anchor}">{format_inline(text)}</h3>')
            continue
        if line.startswith("## "):
            if in_list:
                result.append("</ul>")
                in_list = False
            text = line[3:].strip()
            anchor = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-').lower()
            result.append(f'<h2 id="{anchor}">{format_inline(text)}</h2>')
            continue
        if line.startswith("# "):
            continue  # skip top-level title, handled separately
        
        # Blockquotes
        if line.startswith("> "):
            text = line[2:].strip()
            if text.startswith("**"):
                result.append(f'<blockquote><p>{format_inline(text)}</p></blockquote>')
            else:
                result.append(f'<blockquote><p>{format_inline(text)}</p></blockquote>')
            continue
        
        # List items
        if line.strip().startswith("- "):
            if not in_list:
                result.append("<ul>")
                in_list = True
            text = line.strip()[2:]
            result.append(f"<li>{format_inline(text)}</li>")
            continue
        
        # Horizontal rule
        if line.strip() == "---":
            if in_list:
                result.append("</ul>")
                in_list = False
            result.append("<hr>")
            continue
        
        # Paragraph
        if in_list:
            result.append("</ul>")
            in_list = False
        result.append(f"<p>{format_inline(line)}</p>")
    
    # Close any open elements
    if in_code:
        result.append(f'<pre><code>{html.escape(chr(10).join(code_block))}</code></pre>')
    if in_table:
        result.append('<div class="table-wrap"><table>')
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            result.append("<tr>" + "".join(f"<{tag}>{format_inline(c)}</{tag}>" for c in row) + "</tr>")
        result.append("</table></div>")
    if in_list:
        result.append("</ul>")
    
    return "\n".join(result)

def format_inline(text):
    """Handle inline markdown formatting."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code class="inline">\1</code>', text)
    return text

def get_preamble():
    """Extract the document preamble (before はじめに)."""
    md = read_md()
    idx = md.find("## はじめに")
    if idx == -1:
        return ""
    return md[:idx]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #fafaf8;
  --surface: #ffffff;
  --text: #1a1a1a;
  --text-secondary: #555;
  --accent: #2d5a27;
  --accent-light: #e8f0e6;
  --border: #e0ddd8;
  --code-bg: #f0ede8;
  --nav-bg: #2c2c2c;
  --nav-text: #e0e0e0;
  --nav-active: #a8c99a;
  --blockquote-bg: #f5f3ee;
  --blockquote-border: #c4b99a;
  --table-header: #3a3a3a;
  --table-stripe: #f8f7f4;
  --shadow: rgba(0,0,0,0.06);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  font-family: 'Noto Sans JP', sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 1.85;
  color: var(--text);
  background: var(--bg);
}

/* ===== Layout ===== */
.layout {
  display: flex;
  min-height: 100vh;
}

/* ===== Navigation (Left Sidebar) ===== */
nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  background: var(--nav-bg);
  border-right: 1px solid rgba(255,255,255,0.08);
  box-shadow: 2px 0 12px var(--shadow);
  z-index: 100;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.15) transparent;
}
nav::-webkit-scrollbar { width: 4px; }
nav::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 2px; }

nav .nav-title {
  padding: 24px 20px 16px;
  font-family: 'Noto Serif JP', serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: rgba(255,255,255,0.5);
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

nav .nav-inner {
  display: flex;
  flex-direction: column;
  padding: 8px 0;
}

nav a {
  display: block;
  padding: 10px 20px;
  color: var(--nav-text);
  text-decoration: none;
  font-size: 13px;
  font-weight: 400;
  border-left: 3px solid transparent;
  transition: all 0.2s;
  letter-spacing: 0.02em;
}
nav a:hover { color: #fff; background: rgba(255,255,255,0.06); }
nav a.active {
  color: var(--nav-active);
  border-left-color: var(--nav-active);
  font-weight: 500;
  background: rgba(168,201,154,0.08);
}

/* ===== Main Content ===== */
main {
  margin-left: 200px;
  flex: 1;
  max-width: 840px;
  padding: 48px 48px 96px;
}

/* ===== Typography ===== */
h1 {
  font-family: 'Noto Serif JP', serif;
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 12px;
  color: var(--text);
  letter-spacing: 0.02em;
}

.subtitle {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
  line-height: 1.7;
}

h2 {
  font-family: 'Noto Serif JP', serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 56px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--accent);
  color: var(--text);
  letter-spacing: 0.01em;
}

h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 40px 0 14px;
  color: var(--accent);
  letter-spacing: 0.01em;
}

p {
  margin: 0 0 16px;
}

strong { font-weight: 700; }

/* ===== Code ===== */
pre {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 20px;
  overflow-x: auto;
  margin: 20px 0;
  font-size: 13px;
  line-height: 1.65;
}
pre code {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 400;
  color: var(--text);
}

code.inline {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88em;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 1px 5px;
}

/* ===== Tables ===== */
.table-wrap {
  overflow-x: auto;
  margin: 20px 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
th {
  background: var(--table-header);
  color: #fff;
  font-weight: 500;
  padding: 10px 14px;
  text-align: left;
}
td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
}
tr:nth-child(even) td { background: var(--table-stripe); }

/* ===== Blockquote ===== */
blockquote {
  background: var(--blockquote-bg);
  border-left: 4px solid var(--blockquote-border);
  padding: 16px 20px;
  margin: 20px 0;
  border-radius: 0 6px 6px 0;
}
blockquote p { margin: 0; color: var(--text-secondary); }

/* ===== Lists ===== */
ul {
  margin: 12px 0;
  padding-left: 24px;
}
li { margin-bottom: 6px; }

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 48px 0;
}

/* ===== Page Navigation ===== */
.page-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 64px;
  padding-top: 32px;
  border-top: 1px solid var(--border);
}
.page-nav a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--accent);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 16px;
  border: 1px solid var(--border);
  border-radius: 6px;
  transition: all 0.2s;
}
.page-nav a:hover {
  background: var(--accent-light);
  border-color: var(--accent);
}
.page-nav .spacer { flex: 1; }

/* ===== Index Page ===== */
.toc-list {
  list-style: none;
  padding: 0;
  margin: 32px 0;
}
.toc-list li {
  margin: 0;
  border-bottom: 1px solid var(--border);
}
.toc-list li:first-child { border-top: 1px solid var(--border); }
.toc-list a {
  display: flex;
  align-items: baseline;
  gap: 16px;
  padding: 18px 16px;
  color: var(--text);
  text-decoration: none;
  transition: all 0.15s;
}
.toc-list a:hover { background: var(--accent-light); }
.toc-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 500;
  min-width: 72px;
}
.toc-title { font-weight: 500; }
.toc-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-left: auto;
  text-align: right;
}

/* ===== Responsive ===== */
@media (max-width: 840px) {
  nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 2px 12px var(--shadow);
  }
  nav .nav-title { display: none; }
  nav .nav-inner {
    flex-direction: row;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding: 0;
  }
  nav .nav-inner::-webkit-scrollbar { display: none; }
  nav a {
    padding: 12px 14px;
    font-size: 12px;
    white-space: nowrap;
    border-left: none;
    border-bottom: 2px solid transparent;
  }
  nav a.active {
    border-left-color: transparent;
    border-bottom-color: var(--nav-active);
  }
  main {
    margin-left: 0;
    margin-top: 44px;
    padding: 32px 16px 64px;
  }
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.25rem; }
  .toc-desc { display: none; }
  pre { font-size: 11px; padding: 14px; }
}
"""

def make_page(slug, title, body_html, active_slug):
    """Generate a full HTML page."""
    # Prev/Next navigation
    slugs = [c[0] for c in CHAPTERS]
    idx = slugs.index(slug)
    prev_link = ""
    next_link = ""
    if idx > 0:
        ps, pt = CHAPTERS[idx-1][0], CHAPTERS[idx-1][1]
        prev_link = f'<a href="{ps}.html">← {pt}</a>'
    if idx < len(CHAPTERS) - 1:
        ns, nt = CHAPTERS[idx+1][0], CHAPTERS[idx+1][1]
        next_link = f'<a href="{ns}.html">{nt} →</a>'
    
    nav_links = []
    for nav_slug, nav_label in NAV_ITEMS:
        active = ' class="active"' if nav_slug.replace('.html','') == active_slug else ''
        nav_links.append(f'<a href="{nav_slug}"{active}>{nav_label}</a>')
    nav_html = "\n".join(nav_links)
    
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — AIシステム基盤構造</title>
  <style>{CSS}</style>
</head>
<body>
<div class="layout">
  <nav>
    <div class="nav-title">AIシステム基盤構造</div>
    <div class="nav-inner">
      {nav_html}
    </div>
  </nav>
  <main>
    {body_html}
    <div class="page-nav">
      {prev_link}
      <span class="spacer"></span>
      {next_link}
    </div>
  </main>
</div>
</body>
</html>"""

def build_index_page(preamble_md):
    """Build the index/landing page with TOC."""
    preamble_html = md_to_html_content(preamble_md.strip())
    
    body = f"""
<h1>AIシステム基盤構造</h1>
<p class="subtitle">
  LLMを「使いこなす」ための基礎知識<br>
  <strong>対象読者</strong>: AIを日常的に使っているが、内部の仕組みは詳しくない方<br>
  <strong>目的</strong>: 「なぜAIは指示通りに動かないことがあるのか」を構造的に理解し、より効果的な使い方を身につける
</p>

<h2>目次</h2>
<ul class="toc-list">
  <li><a href="index.html">
    <span class="toc-num">Intro</span>
    <span class="toc-title">はじめに — なぜ「仕組み」を知る必要があるのか</span>
    <span class="toc-desc">AIとの向き合い方</span>
  </a></li>
  <li><a href="chapter1.html">
    <span class="toc-num">Chapter 1</span>
    <span class="toc-title">ステートレス性 — AIは「覚えていない」</span>
    <span class="toc-desc">記憶の正体</span>
  </a></li>
  <li><a href="chapter2.html">
    <span class="toc-num">Chapter 2</span>
    <span class="toc-title">確率的制御と決定論的制御</span>
    <span class="toc-desc">二重構造の核心</span>
  </a></li>
  <li><a href="chapter3.html">
    <span class="toc-num">Chapter 3</span>
    <span class="toc-title">Harness と Context Engineering</span>
    <span class="toc-desc">設計論と対話</span>
  </a></li>
  <li><a href="chapter4.html">
    <span class="toc-num">Chapter 4</span>
    <span class="toc-title">AIシステム基盤構造図</span>
    <span class="toc-desc">全体構造の可視化</span>
  </a></li>
  <li><a href="chapter5.html">
    <span class="toc-num">Chapter 5</span>
    <span class="toc-title">実践への示唆</span>
    <span class="toc-desc">何をどう変えるか</span>
  </a></li>
  <li><a href="chapter6.html">
    <span class="toc-num">Chapter 6</span>
    <span class="toc-title">Harnessの実装 — 機能と実践例</span>
    <span class="toc-desc">Claude Codeでの開発</span>
  </a></li>
  <li><a href="conclusion.html">
    <span class="toc-num">Appendix</span>
    <span class="toc-title">おわりに・用語集・参考文献</span>
    <span class="toc-desc"></span>
  </a></li>
</ul>

<hr>
"""
    
    # Add the intro section content
    md = read_md()
    intro_md = extract_section(md, "## はじめに", "## 第1章")
    intro_html = md_to_html_content(intro_md)
    body += intro_html
    
    return body

def main():
    md = read_md()
    
    # Build index page
    preamble = get_preamble()
    index_body = build_index_page(preamble)
    page = make_page("index", "はじめに", index_body, "index")
    with open(f"{OUT_DIR}/index.html", "w") as f:
        f.write(page)
    print("Created index.html")
    
    # Build chapter pages (skip index, already built)
    for slug, title, start, end in CHAPTERS[1:]:
        section_md = extract_section(md, start, end)
        section_html = md_to_html_content(section_md)
        page = make_page(slug, title, section_html, slug)
        with open(f"{OUT_DIR}/{slug}.html", "w") as f:
            f.write(page)
        print(f"Created {slug}.html")

if __name__ == "__main__":
    main()
