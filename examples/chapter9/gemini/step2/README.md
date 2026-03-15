# Gemini CLI 段階2 — GEMINI.md + Rules

実行日: 2026-03-15
構成: GEMINI.md（Rules統合版）。type 7種・relation 8種の許可リスト追加。Skillsなし。
入力: science.adt2760.pdf（Gianni et al., Science 2026）

## 出力の概要

| 指標 | Gemini 段階1 | Gemini 段階2 | 変化 |
|------|-------------|-------------|------|
| ノード数 | 11 | 9 | -2 |
| エッジ数 | 11 | 8 | -3 |
| type種数 | 5/7 | 5/7 | 不変（method/problem依然不使用） |
| relation種数 | 5/8 | 6/8 | +1（causes, compares出現） |
| labelフィールド | なし | なし | 不変 |

## 最重要の発見: Rulesの二方向効果

Rulesは Gemini に対して二つの逆方向の効果をもたらした:

### 1. ノードを減らす（制約として作用）

段階1→2でノードが11→9に減少。消失したノード:
- `spontaneous_emergence` (process) — 「自然界で偶然に機能分子が生じるプロセス」
- `replication_fidelity` (property) — 忠実度の概念自体は残っていない

段階1にあった `origin_of_life` (concept) は段階2でも残存。type制約（7種リスト）がprocess/propertyの数を減らす方向に作用した。

### 2. relation語彙を増やす（教育として作用）

段階1で不使用だった relation が段階2で出現:
- **causes: 0→2件** — `qt45_ribozyme → self_replication` と `self_replication → origin_of_life`
- **compares: 0→1件** — `class_i_polymerase → qt45_ribozyme`

段階1のGeminiは因果関係（causes）を一度も使わず、同じ関係をproducesやsupportsで代用していた。Rulesに `causes: AがBを引き起こす` と明示的に定義したことで、「引き起こす」関係を認識して使うようになった。

## 段階4との重要な対比

| relation | 段階1 | 段階2 | 段階4（全部入り） |
|----------|-------|-------|-------------------|
| causes | 0 | **2** | **0** |
| compares | 0 | **1** | 0 |
| contains | 1 | **1** | 0 |

**causesが段階2で出現し、段階4で再び消えている。** これは段階3（Skills追加）の結果を見ないと原因が特定できないが、可能性が二つある:
1. SKILL.mdの手順が「何をどう抽出するか」を規定することで、自由な関係の探索が制限された
2. 段階4のHooksの存在が、モデルの行動を保守的にさせた

段階3の結果が、この仮説の検証になる。

## type の使用

| type | 段階1 | 段階2 | 変化 |
|------|-------|-------|------|
| entity | 3 | 3 | 不変 |
| process | 3 | 1 | **-2** |
| concept | 2 | 2 | 不変 |
| property | 2 | 2 | 不変 |
| condition | 1 | 1 | 不変 |
| **method** | 0 | 0 | **依然不使用** |
| **problem** | 0 | 0 | **依然不使用** |

Rulesに method（「手法・技術・実験手順」）と problem（「課題・障害・未解決問題」）の定義を明示したにもかかわらず、Geminiは一つも使わなかった。de novo選択（method相当）も鎖阻害問題（problem相当）も抽出されていない。

一方 Codex は段階1（Rules なし）で既に method=1, problem=1 を使い、段階2では method=2, problem=2 に増えている。relation では causes の定義が「教育」として効いたのに、type では method/problem の定義が効かなかった——**relation定義は Gemini に効き、type定義は効かない**。

### なぜ type 定義が効かないか

推測: Gemini は type を「ノード抽出の後に付与する属性」として扱い、relation を「エッジ生成時に選択する語彙」として扱っている。type 定義を「こういうノードを探せ」ではなく「抽出したノードを分類せよ」と解釈しているなら、method/problem type の定義を読んでも「method 型のノードを探しに行く」行動には繋がらない。つまり type 定義は「分類の語彙」として読まれ、relation 定義は「関係の語彙」として読まれた——後者だけが「新しい関係を探す」行動を誘発した。

## ネットワーク構造

段階2でも QT45 中心のスター型構造は維持。8本のエッジのうち3本が `qt45_ribozyme` を source とする。ただし段階1より横接続が少し出た:
- `structural_complexity → self_replication (inhibits)` — 段階1の spontaneous_emergence 経由のチェーンが短縮
- `class_i_polymerase → qt45_ribozyme (compares)` — 新出

## metadata の変化

段階1: title（日本語訳）, description の2フィールドのみ
段階2: title（**英語原題に変更**）, authors（文字列）, description の3フィールド

- title が日本語訳→英語原題に変わった。Rulesに「日本語で記述する」と書いたが、これは「YAML出力のルール」セクション内。title はメタデータなのでRulesの射程と判断したか、あるいは Codex/Claude に合わせた（別モデルの振る舞いを知るはずはないので偶然）。
- authors フィールドが自発的に追加された。段階1にはなかった。Rulesのフォーマット指示が「構造化を促す」方向にわずかに効いた可能性。

## 三ツール段階2 比較サマリ

| | Claude | Codex | Gemini |
|---|---|---|---|
| 段階1→2 変化 | +5 | +2 | **-2** |
| type 7種遵守 | 7/7 | 7/7 | 5/7 |
| relation 8種遵守 | 8/8 | 6/8 | 6/8 |
| Rulesの機能 | 探索ガイド | デフォルト確認 | 制限＋教育（二方向） |

Rulesの効果がモデルごとに質的に異なることが、段階2のデータで明確に裏付けられた。
