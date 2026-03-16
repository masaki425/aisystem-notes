#!/usr/bin/env python3
"""Replace ASCII diagram in Chapter 6 (Agent comparison) with SVG version."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

OLD_CH6 = '''```
Task Tool / Subagents（階層型）:

  Lead ──委任──→ Worker A ──結果──→ Lead
       ──委任──→ Worker B ──結果──→ Lead
  Worker A と Worker B は互いを知らない。

Agent Teams（チーム型）:

  Team Lead ←──→ Teammate A
       ↕              ↕
  Teammate B ←──→ Teammate A
  全員がメールボックスを通じてメッセージを送り合える。
```'''

NEW_CH6 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 400" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-ch6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <!-- ===== 左: Task Tool / Subagents（階層型）===== -->
  <text x="180" y="24" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">Task Tool / Subagents（階層型）</text>
  <!-- Lead -->
  <rect x="112" y="44" width="136" height="40" rx="8" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
  <text x="180" y="69" text-anchor="middle" font-size="13" font-weight="600" fill="#3C3489">Lead</text>
  <!-- Worker A -->
  <rect x="40" y="148" width="120" height="40" rx="8" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="100" y="173" text-anchor="middle" font-size="12" fill="#3C3489">Worker A</text>
  <!-- Worker B -->
  <rect x="200" y="148" width="120" height="40" rx="8" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="260" y="173" text-anchor="middle" font-size="12" fill="#3C3489">Worker B</text>
  <!-- Lead → Worker A (委任) -->
  <line x1="148" y1="84" x2="108" y2="144" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-ch6)"/>
  <text x="106" y="114" font-size="9.5" fill="#534AB7" text-anchor="end">委任</text>
  <!-- Worker A → Lead (結果) -->
  <line x1="128" y1="148" x2="168" y2="88" stroke="#AFA9EC" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-ch6)"/>
  <text x="168" y="114" font-size="9.5" fill="#AFA9EC">結果</text>
  <!-- Lead → Worker B (委任) -->
  <line x1="212" y1="84" x2="252" y2="144" stroke="#534AB7" stroke-width="0.8" marker-end="url(#arr-ch6)"/>
  <text x="252" y="114" font-size="9.5" fill="#534AB7">委任</text>
  <!-- Worker B → Lead (結果) -->
  <line x1="232" y1="148" x2="192" y2="88" stroke="#AFA9EC" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-ch6)"/>
  <text x="194" y="130" font-size="9.5" fill="#AFA9EC" text-anchor="end">結果</text>
  <!-- Worker A ✕ Worker B (互いを知らない) -->
  <line x1="160" y1="168" x2="200" y2="168" stroke="#D3D1C7" stroke-width="0.8" stroke-dasharray="2 3"/>
  <text x="180" y="160" text-anchor="middle" font-size="14" fill="#D3D1C7">✕</text>
  <!-- 注釈 -->
  <text x="180" y="214" text-anchor="middle" font-size="10.5" fill="#888780">Worker同士は互いを知らない</text>
  <text x="180" y="230" text-anchor="middle" font-size="10.5" fill="#888780">（ファイル経由でのみ連携）</text>
  <!-- ===== 右: Agent Teams（チーム型）===== -->
  <text x="540" y="24" text-anchor="middle" font-size="13" font-weight="600" fill="#085041">Agent Teams（チーム型）</text>
  <!-- Team Lead -->
  <rect x="472" y="44" width="136" height="40" rx="8" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
  <text x="540" y="69" text-anchor="middle" font-size="13" font-weight="600" fill="#085041">Team Lead</text>
  <!-- Teammate A -->
  <rect x="400" y="148" width="120" height="40" rx="8" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="460" y="173" text-anchor="middle" font-size="12" fill="#085041">Teammate A</text>
  <!-- Teammate B -->
  <rect x="560" y="148" width="120" height="40" rx="8" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="620" y="173" text-anchor="middle" font-size="12" fill="#085041">Teammate B</text>
  <!-- Team Lead ↔ Teammate A (双方向) -->
  <line x1="498" y1="84" x2="466" y2="144" stroke="#1D9E75" stroke-width="1" marker-start="url(#arr-ch6)" marker-end="url(#arr-ch6)"/>
  <!-- Team Lead ↔ Teammate B (双方向) -->
  <line x1="582" y1="84" x2="614" y2="144" stroke="#1D9E75" stroke-width="1" marker-start="url(#arr-ch6)" marker-end="url(#arr-ch6)"/>
  <!-- Teammate A ↔ Teammate B (双方向) -->
  <line x1="524" y1="168" x2="556" y2="168" stroke="#1D9E75" stroke-width="1" marker-start="url(#arr-ch6)" marker-end="url(#arr-ch6)"/>
  <!-- 注釈 -->
  <text x="540" y="214" text-anchor="middle" font-size="10.5" fill="#888780">全員がメールボックスを通じて</text>
  <text x="540" y="230" text-anchor="middle" font-size="10.5" fill="#888780">メッセージを直接送り合える</text>
  <!-- ===== 中央の区切り線 ===== -->
  <line x1="360" y1="12" x2="360" y2="240" stroke="#D3D1C7" stroke-width="0.5" stroke-dasharray="6 4"/>
  <!-- ===== 下部: 共通点 ===== -->
  <rect x="40" y="260" width="640" height="120" rx="10" fill="#F1EFE8" stroke="#D3D1C7" stroke-width="0.5"/>
  <text x="360" y="284" text-anchor="middle" font-size="12" font-weight="600" fill="#444441">共通: コンテキストは分離されている</text>
  <line x1="60" y1="294" x2="660" y2="294" stroke="#D3D1C7" stroke-width="0.5"/>
  <!-- 左の説明 -->
  <rect x="60" y="308" width="14" height="14" rx="3" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text x="82" y="320" font-size="11" fill="#5F5E5A">階層型: Leadが統括。Workerは結果をLeadに返す。</text>
  <text x="82" y="338" font-size="11" fill="#5F5E5A">　　　　Worker間の連携はファイルシステム経由のみ。</text>
  <!-- 右の説明 -->
  <rect x="60" y="352" width="14" height="14" rx="3" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="82" y="364" font-size="11" fill="#5F5E5A">チーム型: メールボックスでピアツーピア通信が可能。</text>
</svg>'''

with open(MD_PATH, "r") as f:
    content = f.read()

if OLD_CH6 in content:
    content = content.replace(OLD_CH6, NEW_CH6)
    with open(MD_PATH, "w") as f:
        f.write(content)
    print("✅ 第6章 Agent比較図をSVGに置き換えました。")
else:
    print("⚠️ 第6章の図が見つかりませんでした（既に置き換え済みの可能性があります）。")
