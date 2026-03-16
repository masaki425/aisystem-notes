#!/usr/bin/env python3
"""Replace ASCII diagrams in Chapter 8 with SVG versions.
Uses robust matching: finds the ``` block containing a unique marker string."""
import os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

with open(MD_PATH, "r") as f:
    content = f.read()

count = 0

# ============================================================
# Chapter 8.1: 反復サイクル — find ``` block containing "意図の表明（提案書）" and "閾値を満たした"
# ============================================================
cycle_marker = "意図の表明（提案書）"
cycle_end_marker = "閾値を満たした"

# Find ``` blocks
code_blocks = list(re.finditer(r'```\n(.*?)\n```', content, re.DOTALL))
cycle_block = None
for m in code_blocks:
    if cycle_marker in m.group(1) and cycle_end_marker in m.group(1):
        cycle_block = m
        break

if cycle_block:
    NEW_CYCLE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 580" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-cy-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-cy-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-cy-mpurple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#7F77DD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-cy-gray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#888780" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <linearGradient id="grad-freedom" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EEEDFE"/>
      <stop offset="100%" stop-color="#E1F5EE"/>
    </linearGradient>
  </defs>
  <rect x="140" y="20" width="220" height="48" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="250" y="40" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">意図の表明</text>
  <text x="250" y="58" text-anchor="middle" font-size="10" fill="#534AB7">提案書</text>
  <text x="372" y="40" font-size="10" fill="#888780">自由度：最大</text>
  <text x="372" y="54" font-size="10" fill="#888780">制御：なし</text>
  <line x1="250" y1="68" x2="250" y2="88" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-cy-purple)"/>
  <rect x="140" y="92" width="220" height="48" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="250" y="112" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">構造化</text>
  <text x="250" y="130" text-anchor="middle" font-size="10" fill="#534AB7">仕様書の生成</text>
  <text x="372" y="112" font-size="10" fill="#888780">自由度：高</text>
  <text x="372" y="126" font-size="10" fill="#888780">制御：確率的</text>
  <line x1="250" y1="140" x2="250" y2="160" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-cy-purple)"/>
  <rect x="140" y="164" width="220" height="48" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
  <text x="250" y="184" text-anchor="middle" font-size="13" font-weight="600" fill="#085041">実装</text>
  <text x="250" y="202" text-anchor="middle" font-size="10" fill="#0F6E56">タスク実行</text>
  <text x="372" y="184" font-size="10" fill="#888780">自由度：低</text>
  <text x="372" y="198" font-size="10" fill="#888780">制御：確率的+決定論的</text>
  <line x1="250" y1="212" x2="250" y2="232" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-cy-teal)"/>
  <rect x="140" y="236" width="220" height="48" rx="8" fill="#F1EFE8" stroke="#888780" stroke-width="0.8"/>
  <text x="250" y="256" text-anchor="middle" font-size="13" font-weight="600" fill="#444441">評価</text>
  <text x="250" y="274" text-anchor="middle" font-size="10" fill="#888780">人間の判断</text>
  <path d="M360 252 L480 252 L480 188 L360 188" fill="none" stroke="#0F6E56" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-teal)"/>
  <rect x="490" y="210" width="174" height="24" rx="5" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="577" y="226" text-anchor="middle" font-size="10" fill="#085041">実装の範囲内 → 修正</text>
  <path d="M360 260 L540 260 L540 116 L360 116" fill="none" stroke="#534AB7" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-purple)"/>
  <rect x="550" y="168" width="154" height="24" rx="5" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="627" y="184" text-anchor="middle" font-size="10" fill="#3C3489">仕様に起因 → 修正</text>
  <path d="M360 268 L600 268 L600 44 L360 44" fill="none" stroke="#7F77DD" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-cy-mpurple)"/>
  <rect x="610" y="136" width="100" height="24" rx="5" fill="#EEEDFE" stroke="#AFA9EC" stroke-width="0.5"/>
  <text x="660" y="152" text-anchor="middle" font-size="10" fill="#534AB7">意図 → 見直し</text>
  <text x="250" y="304" text-anchor="middle" font-size="10" fill="#888780">閾値を満たした</text>
  <line x1="250" y1="310" x2="250" y2="332" stroke="#888780" stroke-width="1" marker-end="url(#arr-cy-gray)"/>
  <rect x="170" y="336" width="160" height="36" rx="8" fill="#EAF3DE" stroke="#639922" stroke-width="0.8"/>
  <text x="250" y="359" text-anchor="middle" font-size="13" font-weight="600" fill="#3B6D11">完了</text>
  <rect x="40" y="20" width="8" height="264" rx="4" fill="url(#grad-freedom)"/>
  <text x="56" y="100" font-size="9" fill="#534AB7">自</text>
  <text x="56" y="112" font-size="9" fill="#534AB7">由</text>
  <text x="56" y="124" font-size="9" fill="#534AB7">度</text>
  <text x="40" y="156" font-size="9" fill="#888780">高</text>
  <text x="40" y="168" font-size="9" fill="#888780">↓</text>
  <text x="40" y="180" font-size="9" fill="#888780">低</text>
  <rect x="40" y="400" width="640" height="164" rx="10" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="360" y="424" text-anchor="middle" font-size="12" font-weight="600" fill="#444441">「どこに戻るか」= 問題の粒度に応じた自由度に戻る</text>
  <line x1="60" y1="436" x2="660" y2="436" stroke="#D3D1C7" stroke-width="0.5"/>
  <rect x="60" y="452" width="14" height="14" rx="3" fill="#F0FAF5" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="82" y="464" font-size="11" fill="#5F5E5A">実装の範囲内: フォーマット不整合 → Hooks / Skillsの修正で済む</text>
  <rect x="60" y="480" width="14" height="14" rx="3" fill="#F8F7FE" stroke="#534AB7" stroke-width="0.5"/>
  <text x="82" y="492" font-size="11" fill="#5F5E5A">仕様に起因: タスク分割が不適切 → spec.md / Worker定義を修正</text>
  <rect x="60" y="508" width="14" height="14" rx="3" fill="#EEEDFE" stroke="#7F77DD" stroke-width="0.5"/>
  <text x="82" y="520" font-size="11" fill="#5F5E5A">意図に起因: そもそも作りたいものが違う → proposal.mdから見直し</text>
  <rect x="60" y="536" width="14" height="14" rx="3" fill="#EAF3DE" stroke="#639922" stroke-width="0.5"/>
  <text x="82" y="548" font-size="11" fill="#5F5E5A">閾値を満たした: satisficing → 完了</text>
</svg>'''
    content = content[:cycle_block.start()] + NEW_CYCLE + content[cycle_block.end():]
    count += 1
    print("✅ 第8章 反復サイクル図をSVGに置き換えました。")
elif "arr-cy" in content:
    print("⚠️ 第8章 反復サイクル図は既にSVGに置き換え済みです。")
else:
    print("❌ 第8章 反復サイクル図が見つかりませんでした。")

# ============================================================
# Chapter 8.6: ファイル構成図 — find ``` block containing "CLAUDE.md（プロジェクト概要" and "logs/issues.md"
# ============================================================
files_marker = "CLAUDE.md（プロジェクト概要"
files_end_marker = "logs/issues.md"

# Re-parse code blocks from possibly-modified content
code_blocks = list(re.finditer(r'```\n(.*?)\n```', content, re.DOTALL))
files_block = None
for m in code_blocks:
    if files_marker in m.group(1) and files_end_marker in m.group(1):
        files_block = m
        break

if files_block:
    NEW_FILES = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 620" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-fs-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arr-fs-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="#0F6E56" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <rect x="40" y="16" width="200" height="28" rx="6" fill="#F1EFE8" stroke="#888780" stroke-width="0.5"/>
  <text x="140" y="35" text-anchor="middle" font-size="11" fill="#5F5E5A">CLAUDE.md（概要・ナビゲーション）</text>
  <rect x="40" y="56" width="200" height="36" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="140" y="79" text-anchor="middle" font-size="12" font-weight="600" fill="#3C3489">proposal.md（意図）</text>
  <line x1="140" y1="92" x2="140" y2="118" stroke="#534AB7" stroke-width="1" marker-end="url(#arr-fs-purple)"/>
  <rect x="40" y="122" width="640" height="220" rx="10" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.8"/>
  <rect x="40" y="122" width="640" height="28" rx="10" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.8"/>
  <rect x="40" y="150" width="640" height="0.5" fill="#CECBF6"/>
  <text x="60" y="141" font-size="12" font-weight="600" fill="#3C3489">/setup</text>
  <text x="160" y="141" font-size="10" fill="#534AB7">(.claude/commands/setup.md)</text>
  <rect x="60" y="162" width="184" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="152" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">docs/spec.md</text>
  <text x="152" y="192" text-anchor="middle" font-size="9" fill="#534AB7">仕様</text>
  <rect x="260" y="162" width="184" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="352" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">worker_*.md × 3</text>
  <text x="352" y="192" text-anchor="middle" font-size="9" fill="#534AB7">Worker定義</text>
  <rect x="460" y="162" width="200" height="36" rx="5" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="560" y="177" text-anchor="middle" font-size="10.5" font-weight="500" fill="#3C3489">.claude/rules/</text>
  <text x="560" y="192" text-anchor="middle" font-size="9" fill="#534AB7">行動規則</text>
  <rect x="60" y="210" width="184" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="152" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">validate_phase.py</text>
  <text x="152" y="240" text-anchor="middle" font-size="9" fill="#0F6E56">検証スクリプト</text>
  <rect x="260" y="210" width="184" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="352" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">merge.py</text>
  <text x="352" y="240" text-anchor="middle" font-size="9" fill="#0F6E56">マージスクリプト</text>
  <rect x="460" y="210" width="200" height="36" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="560" y="225" text-anchor="middle" font-size="10.5" font-weight="500" fill="#fff">settings.json</text>
  <text x="560" y="240" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">Stop Hook定義</text>
  <rect x="60" y="258" width="184" height="36" rx="5" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="152" y="273" text-anchor="middle" font-size="10.5" font-weight="500" fill="#444441">docs/progress.md</text>
  <text x="152" y="288" text-anchor="middle" font-size="9" fill="#888780">進捗管理</text>
  <text x="60" y="318" font-size="10" fill="#534AB7">proposal.md → /setup → ファイル一式を自動生成（提案書の変更で一貫して更新）</text>
  <line x1="140" y1="342" x2="140" y2="368" stroke="#0F6E56" stroke-width="1" marker-end="url(#arr-fs-teal)"/>
  <rect x="40" y="372" width="640" height="234" rx="10" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.8"/>
  <rect x="40" y="372" width="640" height="28" rx="10" fill="#E1F5EE" stroke="#9FE1CB" stroke-width="0.8"/>
  <rect x="40" y="400" width="640" height="0.5" fill="#9FE1CB"/>
  <text x="60" y="391" font-size="12" font-weight="600" fill="#085041">/execute</text>
  <text x="160" y="391" font-size="10" fill="#0F6E56">(.claude/commands/execute.md)</text>
  <rect x="60" y="412" width="145" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="132" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">gianni.yaml</text>
  <text x="132" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker A（Phase 1）</text>
  <rect x="218" y="412" width="145" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="290" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">moody.yaml</text>
  <text x="290" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker B（Phase 2）</text>
  <rect x="376" y="412" width="145" height="50" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="448" y="431" text-anchor="middle" font-size="10.5" font-weight="500" fill="#085041">yarus.yaml</text>
  <text x="448" y="449" text-anchor="middle" font-size="9" fill="#0F6E56">Worker C（Phase 3）</text>
  <line x1="132" y1="462" x2="290" y2="478" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <line x1="290" y1="462" x2="290" y2="478" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <line x1="448" y1="462" x2="290" y2="478" stroke="#0F6E56" stroke-width="0.6" stroke-dasharray="3 2"/>
  <rect x="218" y="480" width="145" height="36" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
  <text x="290" y="495" text-anchor="middle" font-size="10.5" font-weight="600" fill="#085041">merged.yaml</text>
  <text x="290" y="510" text-anchor="middle" font-size="9" fill="#0F6E56">Lead（Phase 4）</text>
  <rect x="60" y="530" width="184" height="28" rx="5" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="152" y="549" text-anchor="middle" font-size="10" fill="#444441">docs/progress.md ← 更新</text>
  <rect x="260" y="530" width="184" height="28" rx="5" fill="#FAECE7" stroke="#F0997B" stroke-width="0.5"/>
  <text x="352" y="549" text-anchor="middle" font-size="10" fill="#993C1D">logs/issues.md ← 問題記録</text>
  <rect x="534" y="412" width="130" height="50" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="599" y="432" text-anchor="middle" font-size="10" font-weight="500" fill="#fff">Stop Hook</text>
  <text x="599" y="448" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">progress.md更新</text>
  <text x="599" y="460" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.8)">+ git commitを強制</text>
  <text x="60" y="582" font-size="10" fill="#0F6E56">spec.md + Worker定義に従い実行 → validate_phase.pyで検証 → 問題はissues.mdに自動記録</text>
</svg>'''
    content = content[:files_block.start()] + NEW_FILES + content[files_block.end():]
    count += 1
    print("✅ 第8章 ファイル構成図をSVGに置き換えました。")
elif "arr-fs" in content:
    print("⚠️ 第8章 ファイル構成図は既にSVGに置き換え済みです。")
else:
    print("❌ 第8章 ファイル構成図が見つかりませんでした。")

if count > 0:
    with open(MD_PATH, "w") as f:
        f.write(content)
    print(f"\n合計 {count} 件の図を置き換えて保存しました。")
else:
    print("\n変更はありませんでした。")
