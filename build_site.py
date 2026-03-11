#!/usr/bin/env python3
"""Convert AI architecture lecture markdown into a multi-page HTML site."""


import os, sys, re, html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")
OUT_DIR = SCRIPT_DIR

# Chapter definitions: (slug, title, start_marker, end_marker)
CHAPTERS = [
    ("index", "本稿の位置づけ", "## 本稿の位置づけ", "## はじめに"),
    ("chapter0", "はじめに", "## はじめに", "## 第1章"),
    ("chapter1", "第1章 ステートレス性", "## 第1章", "## 第2章"),
    ("chapter2", "第2章 確率的制御と決定論的制御", "## 第2章", "## 第3章"),
    ("chapter3", "第3章 Harness と Context Engineering", "## 第3章", "## 第4章"),
    ("chapter4", "第4章 AIシステム基盤構造図", "## 第4章", "## 第5章"),
    ("chapter5", "第5章 実践への示唆", "## 第5章", "## 第6章"),
    ("chapter6", "第6章 Harnessの機能", "## 第6章", "## 第7章"),
    ("chapter7", "第7章 実践 — シンプルな課題で機能を組み立てる", "## 第7章", "## 第8章"),
    ("chapter8", "第8章 設計原理", "## 第8章", "## 第9章"),
    ("chapter9", "第9章 Harnessの移植", "## 第9章", "## おわりに"),
    ("conclusion", "おわりに・用語集・参考文献", "## おわりに", None),
]

NAV_ITEMS = [
    ("index.html", "本稿の位置づけ", ""),
    ("chapter0.html", "はじめに", ""),
    ("chapter1.html", "第1章", "ステートレス性"),
    ("chapter2.html", "第2章", "確率的制御と決定論的制御"),
    ("chapter3.html", "第3章", "Harness と Context Engineering"),
    ("chapter4.html", "第4章", "基盤構造図"),
    ("chapter5.html", "第5章", "実践への示唆"),
    ("chapter6.html", "第6章", "Harnessの機能"),
    ("chapter7.html", "第7章", "実践演習"),
    ("chapter8.html", "第8章", "設計原理"),
    ("chapter9.html", "第9章", "Harnessの移植"),
    ("conclusion.html", "おわりに", "用語集・参考文献"),
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
  width: 260px;
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
  padding: 24px 20px 18px;
  font-family: 'Noto Serif JP', serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: rgba(255,255,255,0.85);
  letter-spacing: 0.05em;
  line-height: 1.5;
  border-bottom: 1px solid rgba(255,255,255,0.12);
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
nav a .nav-sub {
  display: block;
  font-size: 12.5px;
  font-weight: 400;
  color: rgba(255,255,255,0.6);
  margin-top: 2px;
  line-height: 1.4;
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
  margin-left: 260px;
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
  font-size: 1.1rem;
  color: var(--text);
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
  line-height: 1.8;
}
.subtitle .sub-main {
  display: flex;
  align-items: center;
  gap: 16px;
  font-family: 'Noto Serif JP', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 14px;
  letter-spacing: 0.03em;
}
.subtitle .sub-main::before {
  content: '';
  width: 24px;
  height: 1px;
  background: var(--border);
}
.subtitle .sub-main::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
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
    for nav_slug, nav_label, nav_subtitle in NAV_ITEMS:
        active = ' class="active"' if nav_slug.replace('.html','') == active_slug else ''
        subtitle_html = f'<span class="nav-sub">{nav_subtitle}</span>' if nav_subtitle else ''
        nav_links.append(f'<a href="{nav_slug}"{active}>{nav_label}{subtitle_html}</a>')
    nav_html = "\n".join(nav_links)
    
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — LLMを「使いこなす」ための基礎知識</title>
  <style>{CSS}</style>
</head>
<body>
<div class="layout">
  <nav>
    <div class="nav-title">LLMを「使いこなす」<br>ための基礎知識</div>
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

def build_index_page():
    """Build the index/landing page with title and positioning section."""
    md = read_md()
    intro_md = extract_section(md, "## 本稿の位置づけ", "## はじめに")
    intro_html = md_to_html_content(intro_md)
    
    body = f"""
<h1>LLMを「使いこなす」ための基礎知識</h1>
<p class="subtitle">
  <span class="sub-main">AIシステム基盤構造から理解する</span>
  <strong>対象読者</strong>: AIを日常的に使っているが、内部の仕組みは詳しくない方<br>
  <strong>目的</strong>: 「なぜAIは指示通りに動かないことがあるのか」を構造的に理解し、より効果的な使い方を身につける<br>
  <strong>前提知識</strong>: ChatGPT、Claude、Gemini等のAIチャットを使った経験があること
</p>

{intro_html}
"""
    return body

def main():
    md = read_md()
    
    # Build index page
    index_body = build_index_page()
    page = make_page("index", "本稿の位置づけ", index_body, "index")
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
