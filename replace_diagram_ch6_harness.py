#!/usr/bin/env python3
"""Replace ASCII diagram in Chapter 6 (Harness structure) with SVG version."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

OLD = '''```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    Harness                              ┃
┃                                                         ┃
┃  ┌─────────────────────────────────────────────────┐   ┃
┃  │ Context Engineering（確率的制御）                 │   ┃
┃  │                                                   │   ┃
┃  │  CLAUDE.md ─── プロジェクト全体の指示             │   ┃
┃  │  Rules     ─── 行動規則・禁止事項                │   ┃
┃  │  Skills    ─── 再利用可能なワークフロー定義       │   ┃
┃  │                                                   │   ┃
┃  │  → すべてテキストとしてコンテキストに注入        │   ┃
┃  │  → モデルへの「影響」（遵守は保証されない）      │   ┃
┃  └─────────────────────────────────────────────────┘   ┃
┃                                                         ┃
┃  ┌─────────────────────────────────────────────────┐   ┃
┃  │ Architectural Constraints（決定論的制御）         │   ┃
┃  │                                                   │   ┃
┃  │  Hooks     ─── ライフサイクルイベントに紐づく     │   ┃
┃  │               スクリプト実行                      │   ┃
┃  │                                                   │   ┃
┃  │  → コードとして実行される                        │   ┃
┃  │  → モデルへの「強制」（遵守が保証される）        │   ┃
┃  └─────────────────────────────────────────────────┘   ┃
┃                                                         ┃
┃  ┌─────────────────────────────────────────────────┐   ┃
┃  │ Agents（タスク分割・並列実行）                    │   ┃
┃  │                                                   │   ┃
┃  │  Worker定義 ─── 役割と指示（確率的制御）          │   ┃
┃  │  Task起動   ─── 別インスタンスの呼び出し          │   ┃
┃  │               （決定論的プロセス）                │   ┃
┃  │                                                   │   ┃
┃  │  → 確率的制御と決定論的制御の両方を含む          │   ┃
┃  │  → コンテキスト分離による容量問題の回避          │   ┃
┃  └─────────────────────────────────────────────────┘   ┃
┃                                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```'''

NEW = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 480" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <!-- Harness 外枠 -->
  <rect x="24" y="12" width="672" height="456" rx="14" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-dasharray="6 3"/>
  <text x="360" y="38" text-anchor="middle" font-size="16" font-weight="600" fill="#3C3489">Harness</text>
  <!-- ===== Context Engineering（確率的制御）===== -->
  <rect x="48" y="56" width="624" height="136" rx="10" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="68" y="78" font-size="13" font-weight="600" fill="#3C3489">Context Engineering（確率的制御）</text>
  <!-- CLAUDE.md -->
  <rect x="68" y="92" width="180" height="48" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="158" y="112" text-anchor="middle" font-size="12" font-weight="500" fill="#3C3489">CLAUDE.md</text>
  <text x="158" y="130" text-anchor="middle" font-size="10" fill="#534AB7">プロジェクト全体の指示</text>
  <!-- Rules -->
  <rect x="268" y="92" width="180" height="48" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="358" y="112" text-anchor="middle" font-size="12" font-weight="500" fill="#3C3489">Rules</text>
  <text x="358" y="130" text-anchor="middle" font-size="10" fill="#534AB7">行動規則・禁止事項</text>
  <!-- Skills -->
  <rect x="468" y="92" width="180" height="48" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="558" y="112" text-anchor="middle" font-size="12" font-weight="500" fill="#3C3489">Skills</text>
  <text x="558" y="130" text-anchor="middle" font-size="10" fill="#534AB7">再利用可能なワークフロー定義</text>
  <!-- 確率的制御の注釈 -->
  <text x="68" y="164" font-size="10.5" fill="#534AB7">→ すべてテキストとしてコンテキストに注入</text>
  <text x="400" y="164" font-size="10.5" fill="#534AB7">→ モデルへの「影響」（遵守は保証されない）</text>
  <!-- ===== Architectural Constraints（決定論的制御）===== -->
  <rect x="48" y="204" width="624" height="100" rx="10" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="68" y="226" font-size="13" font-weight="600" fill="#085041">Architectural Constraints（決定論的制御）</text>
  <!-- Hooks -->
  <rect x="68" y="240" width="580" height="24" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="358" y="256" text-anchor="middle" font-size="11" font-weight="500" fill="#fff">Hooks — ライフサイクルイベントに紐づくスクリプト実行</text>
  <!-- 決定論的制御の注釈 -->
  <text x="68" y="284" font-size="10.5" fill="#0F6E56">→ コードとして実行される</text>
  <text x="400" y="284" font-size="10.5" fill="#0F6E56">→ モデルへの「強制」（遵守が保証される）</text>
  <!-- ===== Agents（複合型）===== -->
  <rect x="48" y="316" width="624" height="140" rx="10" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="68" y="338" font-size="13" font-weight="600" fill="#444441">Agents（タスク分割・並列実行）</text>
  <!-- Worker定義（確率的） -->
  <rect x="68" y="352" width="290" height="48" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="213" y="372" text-anchor="middle" font-size="12" font-weight="500" fill="#3C3489">Worker定義</text>
  <text x="213" y="390" text-anchor="middle" font-size="10" fill="#534AB7">役割と指示（確率的制御）</text>
  <!-- Task起動（決定論的） -->
  <rect x="382" y="352" width="266" height="48" rx="6" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="515" y="372" text-anchor="middle" font-size="12" font-weight="500" fill="#085041">Task起動</text>
  <text x="515" y="390" text-anchor="middle" font-size="10" fill="#0F6E56">別インスタンスの呼び出し（決定論的）</text>
  <!-- Agents の注釈 -->
  <text x="68" y="428" font-size="10.5" fill="#5F5E5A">→ 確率的制御と決定論的制御の両方を含む</text>
  <text x="400" y="428" font-size="10.5" fill="#5F5E5A">→ コンテキスト分離による容量問題の回避</text>
</svg>'''

with open(MD_PATH, "r") as f:
    content = f.read()

if OLD in content:
    content = content.replace(OLD, NEW)
    with open(MD_PATH, "w") as f:
        f.write(content)
    print("✅ 第6章 Harness構成図をSVGに置き換えました。")
else:
    print("⚠️ 第6章 Harness構成図が見つかりませんでした。")
