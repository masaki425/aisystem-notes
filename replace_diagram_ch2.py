#!/usr/bin/env python3
"""Replace ASCII diagram in Chapter 2 with SVG version."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

OLD_BLOCK = '''```
確率的制御                          決定論的制御
(ルール・プロンプト)                (Hooks・コード実行)
─────────────────                   ─────────────────
モデルの内側で作用                  モデルの外側で作用
テキストとして注入                  コードとして実行
「影響を与える」                    「強制する」
遵守率 < 100%                       遵守率 = 100%
スケール容易                        設置コストあり
自由度を活かせる                    自由度を制限する

     │                                    │
     ▼                                    ▼
┌──────────────┐                   ┌──────────────┐
│ 適する場面    │                   │ 適する場面    │
│              │                   │              │
│ ・意図の解釈  │                   │ ・手順遵守    │
│ ・創造的生成  │                   │ ・状態検証    │
│ ・曖昧な指示  │                   │ ・品質ゲート  │
│ ・探索的作業  │                   │ ・必須記録    │
└──────────────┘                   └──────────────┘

     ▲                                    ▲
     │            設計判断                  │
     └──────── ここに何を置くか ────────────┘
               が使いこなしの鍵
```'''

NEW_BLOCK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 520" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-ch2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <g>
    <rect x="40" y="24" width="300" height="52" rx="10" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
    <text x="190" y="44" text-anchor="middle" font-size="15" font-weight="600" fill="#3C3489">確率的制御</text>
    <text x="190" y="64" text-anchor="middle" font-size="11.5" fill="#534AB7">ルール・プロンプト</text>
    <rect x="40" y="92" width="300" height="168" rx="8" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
    <text x="60" y="118" font-size="12.5" fill="#3C3489"><tspan font-weight="400">モデルの</tspan><tspan font-weight="600">内側</tspan><tspan font-weight="400">で作用</tspan></text>
    <text x="60" y="142" font-size="12.5" fill="#3C3489">テキストとして注入</text>
    <text x="60" y="166" font-size="12.5" fill="#3C3489">「影響を与える」</text>
    <text x="60" y="190" font-size="12.5" fill="#3C3489">遵守率 &lt; 100%</text>
    <text x="60" y="214" font-size="12.5" fill="#3C3489">スケール容易</text>
    <text x="60" y="238" font-size="12.5" fill="#3C3489">自由度を活かせる</text>
    <line x1="190" y1="272" x2="190" y2="298" stroke="#534AB7" stroke-width="1.2" marker-end="url(#arr-ch2)"/>
    <rect x="60" y="306" width="260" height="130" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
    <text x="190" y="330" text-anchor="middle" font-size="12.5" font-weight="600" fill="#3C3489">適する場面</text>
    <line x1="80" y1="340" x2="300" y2="340" stroke="#CECBF6" stroke-width="0.5"/>
    <text x="80" y="362" font-size="12" fill="#534AB7">・意図の解釈</text>
    <text x="80" y="384" font-size="12" fill="#534AB7">・創造的生成</text>
    <text x="80" y="406" font-size="12" fill="#534AB7">・曖昧な指示の処理</text>
    <text x="80" y="428" font-size="12" fill="#534AB7">・探索的作業</text>
  </g>
  <g>
    <rect x="380" y="24" width="300" height="52" rx="10" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
    <text x="530" y="44" text-anchor="middle" font-size="15" font-weight="600" fill="#085041">決定論的制御</text>
    <text x="530" y="64" text-anchor="middle" font-size="11.5" fill="#0F6E56">Hooks・コード実行</text>
    <rect x="380" y="92" width="300" height="168" rx="8" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
    <text x="400" y="118" font-size="12.5" fill="#085041"><tspan font-weight="400">モデルの</tspan><tspan font-weight="600">外側</tspan><tspan font-weight="400">で作用</tspan></text>
    <text x="400" y="142" font-size="12.5" fill="#085041">コードとして実行</text>
    <text x="400" y="166" font-size="12.5" fill="#085041">「強制する」</text>
    <text x="400" y="190" font-size="12.5" fill="#085041">遵守率 = 100%</text>
    <text x="400" y="214" font-size="12.5" fill="#085041">設置コストあり</text>
    <text x="400" y="238" font-size="12.5" fill="#085041">自由度を制限する</text>
    <line x1="530" y1="272" x2="530" y2="298" stroke="#0F6E56" stroke-width="1.2" marker-end="url(#arr-ch2)"/>
    <rect x="400" y="306" width="260" height="130" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
    <text x="530" y="330" text-anchor="middle" font-size="12.5" font-weight="600" fill="#085041">適する場面</text>
    <line x1="420" y1="340" x2="640" y2="340" stroke="#9FE1CB" stroke-width="0.5"/>
    <text x="420" y="362" font-size="12" fill="#0F6E56">・手順遵守</text>
    <text x="420" y="384" font-size="12" fill="#0F6E56">・状態検証</text>
    <text x="420" y="406" font-size="12" fill="#0F6E56">・品質ゲート</text>
    <text x="420" y="428" font-size="12" fill="#0F6E56">・必須記録</text>
  </g>
  <line x1="190" y1="444" x2="190" y2="472" stroke="#534AB7" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="530" y1="444" x2="530" y2="472" stroke="#0F6E56" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="190" y1="472" x2="530" y2="472" stroke="#888780" stroke-width="1" stroke-dasharray="4 3"/>
  <line x1="360" y1="472" x2="360" y2="492" stroke="#888780" stroke-width="1.2" marker-end="url(#arr-ch2)"/>
  <text x="360" y="510" text-anchor="middle" font-size="13" font-weight="600" fill="#444441">「ここに何を置くか」が使いこなしの鍵</text>
</svg>'''

with open(MD_PATH, "r") as f:
    content = f.read()

if OLD_BLOCK in content:
    content = content.replace(OLD_BLOCK, NEW_BLOCK)
    with open(MD_PATH, "w") as f:
        f.write(content)
    print("✅ 第2章のASCII図をSVGに置き換えました。")
else:
    print("⚠️ ASCII図が見つかりませんでした（既に置き換え済みの可能性があります）。")
