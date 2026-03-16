#!/usr/bin/env python3
"""Fix SVG arrow markers: replace context-stroke with explicit color markers.

context-stroke is an SVG2 feature with limited browser support.
This script creates color-specific marker definitions for each SVG diagram.
Run AFTER all replace_diagram_*.py scripts have been applied.
"""
import os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

with open(MD_PATH, "r") as f:
    content = f.read()

# Colors used across all diagrams
COLORS = {
    "purple":  "#534AB7",
    "lpurple": "#AFA9EC",
    "mpurple": "#7F77DD",
    "teal":    "#0F6E56",
    "bteal":   "#1D9E75",
    "gray":    "#888780",
    "coral":   "#993C1D",
}

def make_marker(name, color):
    """Generate a marker definition with explicit stroke color."""
    return (
        f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M2 1L8 5L2 9" fill="none" stroke="{color}" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</marker>'
    )

def fix_svg(svg_text):
    """Fix a single SVG block: replace context-stroke markers with color-specific ones."""
    # Find which stroke colors are used with markers
    used_colors = set()
    for m in re.finditer(r'stroke="([^"]+)"[^>]*marker-', svg_text):
        used_colors.add(m.group(1))
    for m in re.finditer(r'marker-(?:end|start)="url\(#[^)]+\)"[^>]*stroke="([^"]+)"', svg_text):
        used_colors.add(m.group(1))
    # Also check lines/paths where stroke comes before marker attrs
    for line in svg_text.split('\n'):
        if 'marker-end' in line or 'marker-start' in line:
            sm = re.search(r'stroke="([^"]+)"', line)
            if sm and sm.group(1) not in ('none',):
                used_colors.add(sm.group(1))

    # Build color→marker-id mapping
    color_to_id = {}
    for color in used_colors:
        for name, hex_val in COLORS.items():
            if color == hex_val:
                color_to_id[color] = f"arr-{name}"
                break
        if color not in color_to_id:
            # Fallback: use hex as part of id (strip #)
            safe = color.lstrip('#')
            color_to_id[color] = f"arr-{safe}"

    if not color_to_id:
        return svg_text

    # Build new defs content
    new_markers = "\n    ".join(make_marker(mid, col) for col, mid in color_to_id.items())

    # Replace existing <defs>...</defs> with new markers
    def replace_defs(m):
        return f"<defs>\n    {new_markers}\n  </defs>"

    svg_text = re.sub(r'<defs>.*?</defs>', replace_defs, svg_text, flags=re.DOTALL)

    # Now update each line/path that uses markers to reference the correct color-specific marker
    def fix_element(m):
        elem = m.group(0)
        stroke_m = re.search(r'stroke="([^"]+)"', elem)
        if not stroke_m:
            return elem
        stroke_color = stroke_m.group(1)
        if stroke_color in color_to_id:
            marker_id = color_to_id[stroke_color]
            # Replace all marker-end/marker-start references
            elem = re.sub(r'marker-end="url\(#[^)]+\)"', f'marker-end="url(#{marker_id})"', elem)
            elem = re.sub(r'marker-start="url\(#[^)]+\)"', f'marker-start="url(#{marker_id})"', elem)
        return elem

    svg_text = re.sub(r'<(?:line|path)[^>]*marker-[^>]*/?>', fix_element, svg_text)

    return svg_text


# Find and fix all inline SVGs
def process_all_svgs(text):
    result = []
    pos = 0
    count = 0
    while True:
        start = text.find('<svg ', pos)
        if start == -1:
            result.append(text[pos:])
            break
        end = text.find('</svg>', start)
        if end == -1:
            result.append(text[pos:])
            break
        end += len('</svg>')

        result.append(text[pos:start])
        svg_block = text[start:end]

        if 'context-stroke' in svg_block:
            svg_block = fix_svg(svg_block)
            count += 1

        result.append(svg_block)
        pos = end

    return ''.join(result), count


content, fixed_count = process_all_svgs(content)

if fixed_count > 0:
    with open(MD_PATH, "w") as f:
        f.write(content)
    print(f"✅ {fixed_count} 個のSVG図の矢印マーカーを修正しました。")
    print("   context-stroke → 色ごとの専用マーカーに置き換え。")
else:
    print("⚠️ context-stroke を含むSVGが見つかりませんでした。")
