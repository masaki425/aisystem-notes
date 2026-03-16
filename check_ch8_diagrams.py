#!/usr/bin/env python3
"""Diagnose why the Chapter 8 diagrams can't be found."""
import os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

with open(MD_PATH, "r") as f:
    content = f.read()

print(f"File size: {len(content)} chars, {content.count(chr(10))} lines")
print()

# 1. Check if SVG already present
for tag in ["arr-cy", "arr-fs", "arr-ch4", "arr-ch2"]:
    if tag in content:
        print(f"  SVG marker '{tag}' FOUND → already replaced")
    else:
        print(f"  SVG marker '{tag}' not found")

print()

# 2. Find all ``` blocks and check their content
blocks = list(re.finditer(r'```[^\n]*\n(.*?)\n```', content, re.DOTALL))
print(f"Total code blocks: {len(blocks)}")
for i, m in enumerate(blocks):
    body = m.group(1)
    if "意図の表明" in body:
        line_num = content[:m.start()].count('\n') + 1
        print(f"\n  Block #{i} at line ~{line_num}: contains '意図の表明'")
        print(f"    Full match: {repr(content[m.start():m.start()+20])}...{repr(content[m.end()-20:m.end()])}")
        print(f"    Body preview: {repr(body[:100])}")
    if "CLAUDE.md（プロジェクト概要" in body:
        line_num = content[:m.start()].count('\n') + 1
        print(f"\n  Block #{i} at line ~{line_num}: contains 'CLAUDE.md（プロジェクト概要'")
        print(f"    Full match: {repr(content[m.start():m.start()+20])}...{repr(content[m.end()-20:m.end()])}")
        print(f"    Body preview: {repr(body[:100])}")

print()

# 3. Check if these are inside SVG tags instead of ``` blocks
for marker in ["意図の表明（提案書）", "CLAUDE.md（プロジェクト概要"]:
    idx = content.find(marker)
    if idx >= 0:
        ctx_start = max(0, idx - 200)
        ctx_end = min(len(content), idx + 100)
        context = content[ctx_start:ctx_end]
        line_num = content[:idx].count('\n') + 1
        # Check if inside SVG
        prev_svg = content.rfind('<svg', 0, idx)
        prev_svg_close = content.rfind('</svg>', 0, idx)
        in_svg = prev_svg > prev_svg_close if prev_svg >= 0 else False
        prev_code = content.rfind('```', 0, idx)
        print(f"  '{marker}' at line ~{line_num}, in_svg={in_svg}")
        print(f"    Nearest ``` before: pos {prev_code}")
        print(f"    Context (200 chars before): ...{repr(content[ctx_start:idx])[-120:]}")
