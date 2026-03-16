#!/usr/bin/env python3
"""Replace ASCII diagrams in Chapter 3 and Chapter 4 with SVG versions."""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

# ============================================================
# Chapter 3: Harness boundary
# ============================================================
OLD_CH3 = '''```
           Harness                        モデル
┌──────────────────────────┐    ┌──────────────────────────┐
│                          │    │                          │
│ オーケストレーション層   │    │ Transformer本体          │
│ Context Engineering      │    │ パラメータ（固定）       │
│ Hooks / ツール実行       │    │ 自己回帰生成             │
│ 外部ガードレール         │    │ 内部ガードレール         │
│ 外部永続化               │    │ (Constitutional AI等)    │
│                          │    │                          │
│ → ユーザーが設計可能     │    │ → ユーザーは変更不可     │
│ → Harness Engineering    │    │ → Model Engineering      │
│   の対象                 │    │   (AI提供者の領域)       │
└──────────────────────────┘    └──────────────────────────┘

馬具（装着・調整できる）         馬（そのものは変えられない）
```'''

NEW_CH3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 360" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <g>
    <rect x="40" y="20" width="300" height="44" rx="10" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.8"/>
    <text x="190" y="48" text-anchor="middle" font-size="15" font-weight="600" fill="#3C3489">Harness</text>
    <rect x="40" y="78" width="300" height="192" rx="8" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
    <text x="60" y="106" font-size="12.5" fill="#3C3489">オーケストレーション層</text>
    <text x="60" y="130" font-size="12.5" fill="#3C3489">Context Engineering</text>
    <text x="60" y="154" font-size="12.5" fill="#3C3489">Hooks / ツール実行</text>
    <text x="60" y="178" font-size="12.5" fill="#3C3489">外部ガードレール</text>
    <text x="60" y="202" font-size="12.5" fill="#3C3489">外部永続化</text>
    <line x1="60" y1="218" x2="320" y2="218" stroke="#CECBF6" stroke-width="0.5"/>
    <text x="60" y="240" font-size="12" font-weight="500" fill="#534AB7">→ ユーザーが設計可能</text>
    <text x="60" y="260" font-size="12" font-weight="500" fill="#534AB7">→ Harness Engineering の対象</text>
    <rect x="60" y="286" width="260" height="30" rx="6" fill="#EEEDFE" stroke="none"/>
    <text x="190" y="306" text-anchor="middle" font-size="12" fill="#534AB7">馬具（装着・調整できる）</text>
  </g>
  <g>
    <rect x="380" y="20" width="300" height="44" rx="10" fill="#FAECE7" stroke="#993C1D" stroke-width="0.8"/>
    <text x="530" y="48" text-anchor="middle" font-size="15" font-weight="600" fill="#712B13">モデル</text>
    <rect x="380" y="78" width="300" height="192" rx="8" fill="#FDF6F3" stroke="#F5C4B3" stroke-width="0.5"/>
    <text x="400" y="106" font-size="12.5" fill="#712B13">Transformer本体</text>
    <text x="400" y="130" font-size="12.5" fill="#712B13">パラメータ（固定）</text>
    <text x="400" y="154" font-size="12.5" fill="#712B13">自己回帰生成</text>
    <text x="400" y="178" font-size="12.5" fill="#712B13">内部ガードレール</text>
    <text x="400" y="202" font-size="12.5" fill="#712B13">(Constitutional AI等)</text>
    <line x1="400" y1="218" x2="660" y2="218" stroke="#F5C4B3" stroke-width="0.5"/>
    <text x="400" y="240" font-size="12" font-weight="500" fill="#993C1D">→ ユーザーは変更不可</text>
    <text x="400" y="260" font-size="12" font-weight="500" fill="#993C1D">→ Model Engineering（AI提供者の領域）</text>
    <rect x="400" y="286" width="260" height="30" rx="6" fill="#FAECE7" stroke="none"/>
    <text x="530" y="306" text-anchor="middle" font-size="12" fill="#993C1D">馬（そのものは変えられない）</text>
  </g>
  <line x1="355" y1="40" x2="355" y2="310" stroke="#B4B2A9" stroke-width="0.5" stroke-dasharray="6 4"/>
  <text x="360" y="340" text-anchor="middle" font-size="12" fill="#888780">← 自分が変えられる範囲 │ 変えられない範囲 →</text>
</svg>'''

# ============================================================
# Chapter 4: 基盤構造図
# ============================================================
OLD_CH4 = '''```
┌─────────────────────────────────────────────────────────────────────┐
│                        ユーザー (Human)                             │
│                                                                     │
│   意図の発生源 ──→ 自然言語入力 ──→ 最終判断者                     │
│   (自由度：高)        (曖昧OK)        (自由度：高)                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ テキスト入力
                           ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                     ┃
┃                    Harness（馬具）                                  ┃
┃                                                                     ┃
┃   モデルの「外側」を包む制御・支援の仕組みの総体                    ┃
┃   確率的制御と決定論的制御の両方を含む                              ┃
┃                                                                     ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │              オーケストレーション層                               │ ┃
┃ │              (決定論的・コード実行)                               │ ┃
┃ │                                                                   │ ┃
┃ │  ┌────────────────────────────────────────────────────────┐      │ ┃
┃ │  │          Context Engineering の対象領域                 │      │ ┃
┃ │  │                                                         │      │ ┃
┃ │  │  ┌───────────┐  ┌──────────────┐  ┌────────────────┐  │      │ ┃
┃ │  │  │ システム   │  │ メモリ注入    │  │ コンテキスト   │  │      │ ┃
┃ │  │  │ プロンプト │+ │ (外部DB検索)  │+ │ ウィンドウ     │  │      │ ┃
┃ │  │  │ 付加       │  │              │  │ 組み立て       │  │      │ ┃
┃ │  │  │            │  │              │  │ (履歴+今回入力)│  │      │ ┃
┃ │  │  └───────────┘  └──────────────┘  └────────────────┘  │      │ ┃
┃ │  │                                                         │      │ ┃
┃ │  │  → コンテキストウィンドウの中身を設計する               │      │ ┃
┃ │  │  → 確率的制御の質を最大化する                           │      │ ┃
┃ │  └────────────────────────────────────────────────────────┘      │ ┃
┃ │                                                                   │ ┃
┃ │  ┌───────────────────────────────────────────────────────────┐   │ ┃
┃ │  │              イベントループ                                │   │ ┃
┃ │  │                                                             │   │ ┃
┃ │  │  ┌───────────────────────────────────────────────────┐     │   │ ┃
┃ │  │  │ ① モデルに入力を送信                               │     │   │ ┃
┃ │  │  └──────────────────────┬────────────────────────────┘     │   │ ┃
┃ │  │                         ▼                                   │   │ ┃
┃ │  │  ┌───────────────────────────────────────────────────┐     │   │ ┃
┃ │  │  │ ② モデルが出力を生成（→ モデル層で処理）          │     │   │ ┃
┃ │  │  └──────────────────────┬────────────────────────────┘     │   │ ┃
┃ │  │                         │                                   │   │ ┃
┃ │  │            ┌────────────┴────────────┐                     │   │ ┃
┃ │  │            ▼                         ▼                     │   │ ┃
┃ │  │     [テキスト応答]          [ツール呼出し要求]              │   │ ┃
┃ │  │            │                         │                     │   │ ┃
┃ │  │            │              ┌──────────▼──────────┐         │   │ ┃
┃ │  │            │              │ ③ PreToolUse Hook   │         │   │ ┃
┃ │  │            │              │   (決定論的チェック)  │         │   │ ┃
┃ │  │            │              └──────────┬──────────┘         │   │ ┃
┃ │  │            │                         ▼                     │   │ ┃
┃ │  │            │              ┌─────────────────────┐         │   │ ┃
┃ │  │            │              │ ④ ツール実行         │         │   │ ┃
┃ │  │            │              │  (Web検索,ファイル操作│         │   │ ┃
┃ │  │            │              │   コード実行 etc.)   │         │   │ ┃
┃ │  │            │              └──────────┬──────────┘         │   │ ┃
┃ │  │            │                         ▼                     │   │ ┃
┃ │  │            │              ┌──────────────────────┐        │   │ ┃
┃ │  │            │              │ ⑤ PostToolUse Hook   │        │   │ ┃
┃ │  │            │              │   (決定論的チェック)   │        │   │ ┃
┃ │  │            │              └──────────┬──────────┘         │   │ ┃
┃ │  │            │                         │                     │   │ ┃
┃ │  │            │              結果をモデルに返す                │   │ ┃
┃ │  │            │                         │                     │   │ ┃
┃ │  │            │                    ②へ戻る                    │   │ ┃
┃ │  │            │                                                │   │ ┃
┃ │  │            ▼                                                │   │ ┃
┃ │  │  ┌───────────────────────────────────────────────────┐     │   │ ┃
┃ │  │  │ ⑥ モデルが「完了」と判断（確率的）                 │     │   │ ┃
┃ │  │  └──────────────────────┬────────────────────────────┘     │   │ ┃
┃ │  │                         ▼                                   │   │ ┃
┃ │  │  ┌───────────────────────────────────────────────────┐     │   │ ┃
┃ │  │  │ ⑦ Stop Hook（決定論的ゲート）                      │     │   │ ┃
┃ │  │  │                                                     │     │   │ ┃
┃ │  │  │  条件チェック ─── 未達 → ②へ差し戻し              │     │   │ ┃
┃ │  │  │                ─── 達成 → 終了許可                 │     │   │ ┃
┃ │  │  └───────────────────────────────────────────────────┘     │   │ ┃
┃ │  └───────────────────────────────────────────────────────────┘   │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                     ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │              外部ガードレール層                                  │ ┃
┃ │              (決定論的・コード実行)                              │ ┃
┃ │                                                                   │ ┃
┃ │  推論時の分類器・フィルタリング                                  │ ┃
┃ │  入出力の安全性チェック                                          │ ┃
┃ │  → モデルの外側で動作する安全機構                               │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                     ┃
┃ ┌─────────────────────────────────────────────────────────────────┐ ┃
┃ │              外部永続化層                                        │ ┃
┃ │              (決定論的・ファイルシステム)                        │ ┃
┃ │                                                                   │ ┃
┃ │  ステートレスなモデルの長期記憶代替                               │ ┃
┃ │  → 外部ファイルに状態を書き出し                                 │ ┃
┃ │  → 次セッションでの読み込みにより記憶を擬似的に継続             │ ┃
┃ └─────────────────────────────────────────────────────────────────┘ ┃
┃                                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                           │
          Harnessの内側 ───┤─── Harnessの外側
          (モデルを包む)   │    (モデルそのもの)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      モデル層（推論エンジン）                        │
│                      ~~~~~~~~~~~~~~~~~~~~~~~~                       │
│                   ★ Harness ではない ★                             │
│                   ★ すべての出力が確率的 ★                         │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 コンテキストウィンドウ (有限)                  │   │
│  │                                                               │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │   │
│  │  │ System   │ │ Memory   │ │ 会話履歴  │ │ 今回の入力     │  │   │
│  │  │ Prompt   │ │ (注入)   │ │ (全ターン)│ │ +ツール結果   │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │   │
│  │                                                               │   │
│  │  ← ウィンドウ上限を超えると古い部分が切り落とされる →         │   │
│  │    (auto-compact: 見えなくなる＝存在しなくなる)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                           │                                         │
│                           ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Transformer (自己回帰生成)                       │   │
│  │                                                               │   │
│  │  トークン₁ → トークン₂ → トークン₃ → ... → トークンₙ       │   │
│  │                                                               │   │
│  │  各ステップで確率分布からサンプリング                         │   │
│  │  P("次のトークン" | これまでの全トークン)                     │   │
│  │                                                               │   │
│  │  ┌───────────────────────────────────────────────────┐       │   │
│  │  │  パラメータ（数千億個の数値）                       │       │   │
│  │  │  ・訓練完了後は固定（会話で変化しない）             │       │   │
│  │  │  ・ユーザーとの対話は何も書き込まない               │       │   │
│  │  │  ・→ ステートレス（状態を持たない）                │       │   │
│  │  └───────────────────────────────────────────────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              内部ガードレール                                 │   │
│  │                                                               │   │
│  │  訓練時に組み込まれた安全性の振る舞い                        │   │
│  │  (Constitutional AI, RLHF による調整)                        │   │
│  │  → モデル自体の性質（確率的に作用）                          │   │
│  │  → Harness ではない                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```'''

NEW_CH4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 1060" style="max-width:720px;width:100%;height:auto;display:block;margin:24px auto" font-family="'Noto Sans JP','Hiragino Sans',sans-serif">
  <defs>
    <marker id="arr-ch4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
  <!-- ===== ユーザー ===== -->
  <rect x="40" y="16" width="640" height="56" rx="10" fill="#F1EFE8" stroke="#888780" stroke-width="0.8"/>
  <text x="360" y="38" text-anchor="middle" font-size="14" font-weight="600" fill="#2C2C2A">ユーザー (Human)</text>
  <text x="360" y="60" text-anchor="middle" font-size="11" fill="#5F5E5A">意図の発生源 → 自然言語入力 → 最終判断者</text>
  <!-- 矢印: ユーザー → Harness -->
  <line x1="360" y1="72" x2="360" y2="96" stroke="#888780" stroke-width="1.2" marker-end="url(#arr-ch4)"/>
  <text x="370" y="88" font-size="10" fill="#888780">テキスト入力</text>
  <!-- ===== Harness 外枠 ===== -->
  <rect x="24" y="100" width="672" height="584" rx="14" fill="none" stroke="#534AB7" stroke-width="1.5" stroke-dasharray="6 3"/>
  <text x="360" y="122" text-anchor="middle" font-size="15" font-weight="600" fill="#3C3489">Harness（馬具）</text>
  <text x="360" y="140" text-anchor="middle" font-size="10.5" fill="#534AB7">モデルの「外側」を包む制御・支援の仕組みの総体</text>
  <!-- --- Context Engineering --- -->
  <rect x="48" y="154" width="624" height="112" rx="8" fill="#F8F7FE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="68" y="174" font-size="12" font-weight="600" fill="#3C3489">Context Engineering の対象領域（確率的制御）</text>
  <rect x="68" y="186" width="180" height="64" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="158" y="210" text-anchor="middle" font-size="11" font-weight="500" fill="#3C3489">システムプロンプト</text>
  <text x="158" y="228" text-anchor="middle" font-size="10" fill="#534AB7">付加</text>
  <text x="260" y="218" font-size="14" fill="#CECBF6">+</text>
  <rect x="276" y="186" width="180" height="64" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="366" y="210" text-anchor="middle" font-size="11" font-weight="500" fill="#3C3489">メモリ注入</text>
  <text x="366" y="228" text-anchor="middle" font-size="10" fill="#534AB7">(外部DB検索)</text>
  <text x="468" y="218" font-size="14" fill="#CECBF6">+</text>
  <rect x="484" y="186" width="172" height="64" rx="6" fill="#EEEDFE" stroke="#CECBF6" stroke-width="0.5"/>
  <text x="570" y="210" text-anchor="middle" font-size="11" font-weight="500" fill="#3C3489">コンテキスト</text>
  <text x="570" y="228" text-anchor="middle" font-size="10" fill="#534AB7">ウィンドウ組み立て</text>
  <!-- --- イベントループ --- -->
  <rect x="48" y="278" width="624" height="304" rx="8" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="68" y="298" font-size="12" font-weight="600" fill="#085041">イベントループ（オーケストレーション層）</text>
  <!-- ① 入力送信 -->
  <rect x="220" y="310" width="280" height="28" rx="6" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="360" y="329" text-anchor="middle" font-size="11" fill="#085041">① モデルに入力を送信</text>
  <line x1="360" y1="338" x2="360" y2="352" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- ② 出力生成 -->
  <rect x="220" y="356" width="280" height="28" rx="6" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="360" y="375" text-anchor="middle" font-size="11" fill="#085041">② モデルが出力を生成</text>
  <!-- 分岐 -->
  <line x1="280" y1="384" x2="280" y2="404" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <line x1="440" y1="384" x2="440" y2="404" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- 左: テキスト応答 -->
  <rect x="188" y="408" width="184" height="24" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="280" y="425" text-anchor="middle" font-size="10.5" fill="#085041">テキスト応答</text>
  <line x1="280" y1="432" x2="280" y2="490" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- 右: ツール呼出し -->
  <rect x="350" y="408" width="184" height="24" rx="5" fill="#E1F5EE" stroke="#5DCAA5" stroke-width="0.5"/>
  <text x="442" y="425" text-anchor="middle" font-size="10.5" fill="#085041">ツール呼出し要求</text>
  <line x1="442" y1="432" x2="442" y2="446" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- ③ PreToolUse -->
  <rect x="370" y="450" width="144" height="24" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="442" y="466" text-anchor="middle" font-size="10" font-weight="500" fill="#fff">③ PreToolUse Hook</text>
  <line x1="442" y1="474" x2="442" y2="484" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- ④ ツール実行 -->
  <rect x="370" y="488" width="144" height="24" rx="5" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="442" y="504" text-anchor="middle" font-size="10" fill="#085041">④ ツール実行</text>
  <line x1="442" y1="512" x2="442" y2="522" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- ⑤ PostToolUse -->
  <rect x="370" y="526" width="144" height="24" rx="5" fill="#1D9E75" stroke="none"/>
  <text x="442" y="542" text-anchor="middle" font-size="10" font-weight="500" fill="#fff">⑤ PostToolUse Hook</text>
  <!-- ツール結果→②へ戻る -->
  <path d="M514 538 L580 538 L580 370 L500 370" fill="none" stroke="#0F6E56" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-ch4)"/>
  <text x="590" y="454" font-size="9" fill="#0F6E56" transform="rotate(90,590,454)">②へ戻る</text>
  <!-- ⑥ 完了判断 -->
  <rect x="188" y="494" width="184" height="28" rx="6" fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5"/>
  <text x="280" y="512" text-anchor="middle" font-size="10.5" fill="#085041">⑥「完了」と判断（確率的）</text>
  <line x1="280" y1="522" x2="280" y2="536" stroke="#0F6E56" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- ⑦ Stop Hook -->
  <rect x="188" y="540" width="184" height="28" rx="6" fill="#1D9E75" stroke="none"/>
  <text x="280" y="558" text-anchor="middle" font-size="10.5" font-weight="500" fill="#fff">⑦ Stop Hook（決定論的）</text>
  <!-- Stop Hook 分岐 -->
  <text x="180" y="562" text-anchor="end" font-size="9" fill="#085041">未達→②へ差し戻し</text>
  <path d="M188 554 L120 554 L120 370 L218 370" fill="none" stroke="#0F6E56" stroke-width="0.8" stroke-dasharray="4 2" marker-end="url(#arr-ch4)"/>
  <text x="380" y="575" font-size="9" fill="#085041">達成→終了許可</text>
  <!-- --- 外部ガードレール層 --- -->
  <rect x="48" y="594" width="300" height="40" rx="6" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="198" y="612" text-anchor="middle" font-size="11" font-weight="500" fill="#085041">外部ガードレール層</text>
  <text x="198" y="628" text-anchor="middle" font-size="9.5" fill="#0F6E56">入出力の安全性チェック</text>
  <!-- --- 外部永続化層 --- -->
  <rect x="372" y="594" width="300" height="40" rx="6" fill="#F0FAF5" stroke="#9FE1CB" stroke-width="0.5"/>
  <text x="522" y="612" text-anchor="middle" font-size="11" font-weight="500" fill="#085041">外部永続化層</text>
  <text x="522" y="628" text-anchor="middle" font-size="9.5" fill="#0F6E56">ファイルに状態を書き出し</text>
  <!-- ===== 境界表示 ===== -->
  <line x1="40" y1="700" x2="680" y2="700" stroke="#B4B2A9" stroke-width="0.8" stroke-dasharray="6 4"/>
  <text x="200" y="716" text-anchor="end" font-size="10" fill="#888780">Harnessの内側（モデルを包む）</text>
  <text x="520" y="716" text-anchor="start" font-size="10" fill="#888780">Harnessの外側（モデルそのもの）</text>
  <line x1="360" y1="700" x2="360" y2="736" stroke="#888780" stroke-width="1" marker-end="url(#arr-ch4)"/>
  <!-- ===== モデル層 ===== -->
  <rect x="40" y="740" width="640" height="304" rx="12" fill="#FDF6F3" stroke="#993C1D" stroke-width="1"/>
  <text x="360" y="764" text-anchor="middle" font-size="14" font-weight="600" fill="#712B13">モデル層（推論エンジン）</text>
  <text x="360" y="782" text-anchor="middle" font-size="10" fill="#993C1D">★ Harnessではない ★ すべての出力が確率的 ★</text>
  <!-- コンテキストウィンドウ -->
  <rect x="64" y="796" width="592" height="96" rx="8" fill="#FAECE7" stroke="#F0997B" stroke-width="0.5"/>
  <text x="360" y="816" text-anchor="middle" font-size="11" font-weight="500" fill="#712B13">コンテキストウィンドウ（有限）</text>
  <rect x="84" y="826" width="124" height="32" rx="5" fill="#F5C4B3" stroke="none"/>
  <text x="146" y="846" text-anchor="middle" font-size="10" fill="#712B13">System Prompt</text>
  <rect x="218" y="826" width="108" height="32" rx="5" fill="#F5C4B3" stroke="none"/>
  <text x="272" y="846" text-anchor="middle" font-size="10" fill="#712B13">Memory (注入)</text>
  <rect x="336" y="826" width="108" height="32" rx="5" fill="#F5C4B3" stroke="none"/>
  <text x="390" y="846" text-anchor="middle" font-size="10" fill="#712B13">会話履歴</text>
  <rect x="454" y="826" width="124" height="32" rx="5" fill="#F5C4B3" stroke="none"/>
  <text x="516" y="846" text-anchor="middle" font-size="10" fill="#712B13">今回の入力</text>
  <text x="360" y="880" text-anchor="middle" font-size="9" fill="#993C1D">← 上限を超えると古い部分が切り落とされる (auto-compact) →</text>
  <!-- 矢印 -->
  <line x1="360" y1="892" x2="360" y2="910" stroke="#993C1D" stroke-width="0.8" marker-end="url(#arr-ch4)"/>
  <!-- Transformer -->
  <rect x="64" y="914" width="592" height="64" rx="8" fill="#FAECE7" stroke="#F0997B" stroke-width="0.5"/>
  <text x="84" y="934" font-size="11" font-weight="500" fill="#712B13">Transformer（自己回帰生成）</text>
  <text x="84" y="952" font-size="10" fill="#993C1D">トークン₁ → トークン₂ → … → トークンₙ　　各ステップで確率分布からサンプリング</text>
  <text x="84" y="968" font-size="10" fill="#993C1D">パラメータ: 訓練完了後は固定 → ステートレス（会話で変化しない）</text>
  <!-- 内部ガードレール -->
  <rect x="64" y="990" width="592" height="40" rx="6" fill="#FAECE7" stroke="#F0997B" stroke-width="0.5"/>
  <text x="84" y="1010" font-size="11" font-weight="500" fill="#712B13">内部ガードレール</text>
  <text x="310" y="1010" font-size="10" fill="#993C1D">(Constitutional AI, RLHF) → Harnessではない</text>
  <!-- 凡例 -->
  <rect x="80" y="650" width="10" height="10" rx="2" fill="#EEEDFE" stroke="#534AB7" stroke-width="0.5"/>
  <text x="96" y="660" font-size="9.5" fill="#534AB7">確率的制御</text>
  <rect x="220" y="650" width="10" height="10" rx="2" fill="#1D9E75" stroke="none"/>
  <text x="236" y="660" font-size="9.5" fill="#085041">決定論的制御 (Hooks)</text>
  <rect x="420" y="650" width="10" height="10" rx="2" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
  <text x="436" y="660" font-size="9.5" fill="#993C1D">モデル層（変更不可）</text>
</svg>'''

# ============================================================
# Apply replacements
# ============================================================
with open(MD_PATH, "r") as f:
    content = f.read()

count = 0

if OLD_CH3 in content:
    content = content.replace(OLD_CH3, NEW_CH3)
    count += 1
    print("✅ 第3章 Harness境界図をSVGに置き換えました。")
else:
    print("⚠️ 第3章の図が見つかりませんでした。")

if OLD_CH4 in content:
    content = content.replace(OLD_CH4, NEW_CH4)
    count += 1
    print("✅ 第4章 基盤構造図をSVGに置き換えました。")
else:
    print("⚠️ 第4章の図が見つかりませんでした。")

if count > 0:
    with open(MD_PATH, "w") as f:
        f.write(content)
    print(f"\n合計 {count} 件の図を置き換えて保存しました。")
else:
    print("\n変更はありませんでした。")
