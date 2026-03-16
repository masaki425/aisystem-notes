#!/usr/bin/env python3
"""
Fix Chapter 8 SVG diagrams: replace existing SVGs with overlap-free versions.

Targets:
1. Section 8.1 cycle diagram (contains "意図の表明" + "閾値を満たした")
2. Section 8.6 file structure diagram (contains "proposal.md（意図）" + "/execute")
"""
import re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

# ── New SVGs ──────────────────────────────────────────────

NEW_CYCLE_SVG = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 580" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-cy-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <marker id="arr-cy-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <marker id="arr-cy-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#888780" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <marker id="arr-cy-mpurple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#7F77DD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <linearGradient id="grad-cy-freedom" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EEEDFE"/><stop offset="100%" stop-color="#E1F5EE"/>
    </linearGradient>
  </defs>
  <!-- ===== 自由度グラデーションバー（左端）===== -->
  <rect x="40" y="24" width="8" height="280" rx="4" fill="url(#grad-cy-freedom)"/>
  <text x="32" y="100" font-size="9" fill="#534AB7" text-anchor="end">高</text>
  <text x="32" y="200" font-size="9" fill="#888780" text-anchor="end">↓</text>
  <text x="32" y="280" font-size="9" fill="#0F6E56" text-anchor="end">低</text>
  <text x="56" y="155" font-size="9" fill="#888780">自由度</text>
  <!-- ===== 4段階ボックス（左寄せ）===== -->
  <!-- 意図の表明 -->
  <rect x="80" y="24" width="240" height="48" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="200" y="43" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">意図の表明</text>
  <text x="200" y="62" text-anchor="middle" font-size="10" fill="#534AB7">提案書</text>
  <text x="332" y="43" font-size="9.5" fill="#888780">自由度：最大</text>
  <text x="332" y="57" font-size="9.5" fill="#888780">制御：なし</text>
  <!-- 矢印 -->
  <line x1="200" y1="72" x2="200" y2="94" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-cy-purple)"/>
  <!-- 構造化 -->
  <rect x="80" y="98" width="240" height="48" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="200" y="117" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">構造化</text>
  <text x="200" y="136" text-anchor="middle" font-size="10" fill="#534AB7">仕様書の生成</text>
  <text x="332" y="117" font-size="9.5" fill="#888780">自由度：高</text>
  <text x="332" y="131" font-size="9.5" fill="#888780">制御：確率的</text>
  <!-- 矢印 -->
  <line x1="200" y1="146" x2="200" y2="168" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-cy-purple)"/>
  <!-- 実装 -->
  <rect x="80" y="172" width="240" height="48" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
  <text x="200" y="191" text-anchor="middle" font-size="13" font-weight="600" fill="#085041">実装</text>
  <text x="200" y="210" text-anchor="middle" font-size="10" fill="#0F6E56">タスク実行</text>
  <text x="332" y="191" font-size="9.5" fill="#888780">自由度：低</text>
  <text x="332" y="205" font-size="9.5" fill="#888780">制御：確率的+決定論的</text>
  <!-- 矢印 -->
  <line x1="200" y1="220" x2="200" y2="242" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-cy-teal)"/>
  <!-- 評価 -->
  <rect x="80" y="246" width="240" height="48" rx="8" fill="#F1EFE8" stroke="#888780" stroke-width="0.8"/>
  <text x="200" y="265" text-anchor="middle" font-size="13" font-weight="600" fill="#444441">評価</text>
  <text x="200" y="284" text-anchor="middle" font-size="10" fill="#888780">人間の判断</text>
  <!-- ===== フィードバック矢印（右側・段階的に外側へ）===== -->
  <!-- 評価→実装（最短ループ x=480）-->
  <path d="M320 270 L480 270 L480 196 L320 196" fill="none" stroke="#0F6E56" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-teal)"/>
  <!-- ラベル：矢印の折り返し地点の右 -->
  <text x="490" y="237" font-size="9.5" fill="#085041">実装の範囲内</text>
  <text x="490" y="250" font-size="9.5" fill="#085041">→ 修正</text>
  <!-- 評価→構造化（中ループ x=545）-->
  <path d="M320 276 L545 276 L545 122 L320 122" fill="none" stroke="#534AB7" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-purple)"/>
  <text x="555" y="200" font-size="9.5" fill="#3C3489">仕様に起因</text>
  <text x="555" y="213" font-size="9.5" fill="#3C3489">→ 修正</text>
  <!-- 評価→意図（最長ループ x=610）-->
  <path d="M320 282 L610 282 L610 48 L320 48" fill="none" stroke="#7F77DD" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-mpurple)"/>
  <text x="620" y="166" font-size="9.5" fill="#534AB7">意図に起因</text>
  <text x="620" y="179" font-size="9.5" fill="#534AB7">→ 見直し</text>
  <!-- ===== 完了（下へ）===== -->
  <line x1="200" y1="294" x2="200" y2="330" stroke="#888780" stroke-width="1" marker-end="url(#arr-cy-gray)"/>
  <text x="200" y="324" text-anchor="middle" font-size="10" fill="#888780">閾値を満たした</text>
  <rect x="130" y="338" width="140" height="36" rx="8" fill="#EAF3DE" stroke="#639922" stroke-width="0.8"/>
  <text x="200" y="361" text-anchor="middle" font-size="13" font-weight="600" fill="#3B6D11">完了</text>
  <!-- ===== 凡例 ===== -->
  <rect x="40" y="400" width="640" height="168" rx="10" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="360" y="424" text-anchor="middle" font-size="12" font-weight="600" fill="#444441">「どこに戻るか」= 問題の粒度に応じた自由度に戻る</text>
  <line x1="60" y1="434" x2="660" y2="434" stroke="#D3D1C7" stroke-width="0.5"/>
  <rect x="60" y="448" width="14" height="14" rx="3" fill="#F0FAF5" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="82" y="460" font-size="11" fill="#5F5E5A">実装の範囲内: フォーマット不整合 → Hooks / Skillsの修正で済む</text>
  <rect x="60" y="476" width="14" height="14" rx="3" fill="#F8F7FE" stroke="#534AB7" stroke-width="0.5"/>
  <text x="82" y="488" font-size="11" fill="#5F5E5A">仕様に起因: タスク分割が不適切 → spec.md / Worker定義を修正</text>
  <rect x="60" y="504" width="14" height="14" rx="3" fill="#EEEDFE" stroke="#7F77DD" stroke-width="0.5"/>
  <text x="82" y="516" font-size="11" fill="#5F5E5A">意図に起因: そもそも作りたいものが違う → proposal.mdから見直し</text>
  <rect x="60" y="532" width="14" height="14" rx="3" fill="#EAF3DE" stroke="#639922" stroke-width="0.5"/>
  <text x="82" y="544" font-size="11" fill="#5F5E5A">閾値を満たした: satisficing → 完了</text>
</svg>'''

NEW_FILESTRUCT_SVG = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 620" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-fs-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <marker id="arr-fs-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
  </defs>
  <!-- ===== 起点: proposal.md + CLAUDE.md ===== -->
  <rect x="40" y="16" width="200" height="28" rx="6" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
  <text x="140" y="35" text-anchor="middle" font-size="11" fill="#5F5E5A">CLAUDE.md（概要・ナビゲーション）</text>
  <rect x="40" y="56" width="200" height="36" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="140" y="79" text-anchor="middle" font-size="12" font-weight="600" fill="#3C3489">proposal.md（意図）</text>
  <line x1="140" y1="92" x2="140" y2="118" stroke="#534AB7" stroke-width="1" marker-end="url(#arr-fs-purple)"/>
  <!-- ===== /setup フェーズ ===== -->
  <rect x="40" y="122" width="640" height="220" rx="10" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.8"/>
  <rect x="40" y="122" width="640" height="28" rx="10" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.8"/>
  <rect x="40" y="150" width="640" height="0.5" fill="#CECBF6"/>
  <text x="60" y="141" font-size="12" font-weight="600" fill="#3C3489">/setup</text>
  <text x="160" y="141" font-size="10" fill="#534AB7">(.claude/commands/setup.md)</text>
  <!-- 生成ファイル群 1行目 -->
  <rect x="60" y="162" width="184" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="152" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">docs/spec.md</text>
  <text x="152" y="192" text-anchor="middle" font-size="9" fill="#534AB7">仕様</text>
  <rect x="260" y="162" width="184" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="352" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">worker_*.md × 3</text>
  <text x="352" y="192" text-anchor="middle" font-size="9" fill="#534AB7">Worker定義</text>
  <rect x="460" y="162" width="200" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="560" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">.claude/rules/</text>
  <text x="560" y="192" text-anchor="middle" font-size="9" fill="#534AB7">行動規則</text>
  <!-- 2行目 -->
  <rect x="60" y="210" width="184" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="152" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">validate_phase.py</text>
  <text x="152" y="240" text-anchor="middle" font-size="9" fill="#0F6E56">検証スクリプト</text>
  <rect x="260" y="210" width="184" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="352" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">merge.py</text>
  <text x="352" y="240" text-anchor="middle" font-size="9" fill="#0F6E56">マージスクリプト</text>
  <rect x="460" y="210" width="200" height="36" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="560" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#fff">settings.json</text>
  <text x="560" y="240" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">Stop Hook定義</text>
  <!-- 3行目 -->
  <rect x="60" y="258" width="184" height="36" rx="5" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="152" y="273" text-anchor="middle" font-size="10.5" font-weight="500" fill="#444441">docs/progress.md</text>
  <text x="152" y="288" text-anchor="middle" font-size="9" fill="#888780">進捗管理</text>
  <!-- 注釈 -->
  <text x="60" y="318" font-size="10" fill="#534AB7">proposal.md → /setup → ファイル一式を自動生成（提案書の変更で一貫して更新）</text>
  <!-- 矢印 /setup → /execute -->
  <line x1="140" y1="342" x2="140" y2="368" stroke="#0F6E56" stroke-width="1" marker-end="url(#arr-fs-teal)"/>
  <!-- ===== /execute フェーズ ===== -->
  <rect x="40" y="372" width="640" height="234" rx="10" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.8"/>
  <rect x="40" y="372" width="640" height="28" rx="10" fill="#E1F5EE" stroke="#9FE1CB" stroke-width="0.8"/>
  <rect x="40" y="400" width="640" height="0.5" fill="#9FE1CB"/>
  <text x="60" y="391" font-size="12" font-weight="600" fill="#085041">/execute</text>
  <text x="160" y="391" font-size="10" fill="#0F6E56">(.claude/commands/execute.md)</text>
  <!-- Worker出力 -->
  <rect x="60" y="412" width="135" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="127" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">gianni.yaml</text>
  <text x="127" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker A</text>
  <rect x="208" y="412" width="135" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="275" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">moody.yaml</text>
  <text x="275" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker B</text>
  <rect x="356" y="412" width="135" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="423" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">yarus.yaml</text>
  <text x="423" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker C</text>
  <!-- 矢印 3つ → merged -->
  <line x1="127" y1="462" x2="275" y2="480" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <line x1="275" y1="462" x2="275" y2="480" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <line x1="423" y1="462" x2="275" y2="480" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <!-- merged.yaml -->
  <rect x="208" y="484" width="135" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
  <text x="275" y="499" text-anchor="middle" font-size="10.5" font-weight="600" fill="#085041">merged.yaml</text>
  <text x="275" y="514" text-anchor="middle" font-size="9" fill="#0F6E56">Lead（Phase 4）</text>
  <!-- progress + issues -->
  <rect x="60" y="534" width="184" height="28" rx="5" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="152" y="553" text-anchor="middle" font-size="10" fill="#444441">docs/progress.md ← 更新</text>
  <rect x="260" y="534" width="184" height="28" rx="5" fill="#FAECE7" stroke="#F0997B" stroke-width="0.5"/>
  <text x="352" y="553" text-anchor="middle" font-size="10" fill="#993C1D">logs/issues.md ← 問題記録</text>
  <!-- Stop Hook -->
  <rect x="510" y="412" width="150" height="50" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="585" y="432" text-anchor="middle" font-size="10" font-weight="500" fill="#fff">Stop Hook</text>
  <text x="585" y="448" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">progress.md更新</text>
  <text x="585" y="460" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">+ git commitを強制</text>
  <!-- 注釈 -->
  <text x="60" y="586" font-size="10" fill="#0F6E56">spec.md + Worker定義に従い実行 → validate_phase.pyで検証 → 問題はissues.mdに自動記録</text>
</svg>'''


def main():
    with open(MD_PATH, "r") as f:
        content = f.read()

    # Find all <svg>...</svg> blocks
    svg_pattern = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL)
    svgs = list(svg_pattern.finditer(content))
    print(f"Found {len(svgs)} SVG blocks total")

    replaced_cycle = False
    replaced_filestruct = False

    # Process in reverse order to preserve positions
    for m in reversed(svgs):
        svg_text = m.group(0)

        # Identify cycle diagram (section 8.1)
        if "意図の表明" in svg_text and "閾値を満たした" in svg_text and not replaced_cycle:
            line_num = content[:m.start()].count('\n') + 1
            print(f"  → Cycle diagram at line ~{line_num} (len={len(svg_text)})")

            if "arr-cy" in svg_text:
                print("    Already replaced (arr-cy markers found). Replacing again with latest version.")

            content = content[:m.start()] + NEW_CYCLE_SVG + content[m.end():]
            replaced_cycle = True
            print("    ✅ Replaced with overlap-free version")

        # Identify file structure diagram (section 8.6)
        elif "proposal.md（意図）" in svg_text and "/execute" in svg_text and not replaced_filestruct:
            line_num = content[:m.start()].count('\n') + 1
            print(f"  → File structure diagram at line ~{line_num} (len={len(svg_text)})")

            if "arr-fs" in svg_text:
                print("    Already replaced (arr-fs markers found). Replacing again with latest version.")

            content = content[:m.start()] + NEW_FILESTRUCT_SVG + content[m.end():]
            replaced_filestruct = True
            print("    ✅ Replaced with overlap-free version")

    if replaced_cycle or replaced_filestruct:
        with open(MD_PATH, "w") as f:
            f.write(content)
        print(f"\n✅ File saved. Replaced: cycle={replaced_cycle}, filestruct={replaced_filestruct}")
    else:
        print("\n❌ No replacements made.")

    if not replaced_cycle:
        print("  Cycle diagram not found. Looking for SVGs with '意図の表明'...")
        for i, m in enumerate(svgs):
            if "意図の表明" in m.group(0):
                print(f"    SVG #{i} contains '意図の表明' but not '閾値を満たした'")
            if "閾値" in m.group(0):
                print(f"    SVG #{i} contains '閾値'")

    if not replaced_filestruct:
        print("  File structure diagram not found. Looking for SVGs with 'proposal.md'...")
        for i, m in enumerate(svgs):
            if "proposal.md" in m.group(0):
                print(f"    SVG #{i} contains 'proposal.md'")


if __name__ == "__main__":
    main()
