# Gemini CLI 段階3 — GEMINI.md + Rules + Skills

実行日: 2026-03-15
構成: GEMINI.md（Rules統合版）+ .gemini/skills/structurize/SKILL.md。Hooksなし。
入力: science.adt2760.pdf（Gianni et al., Science 2026）

## 出力の概要

| 指標 | 段階1 | 段階2 | 段階3 | 段階4 |
|------|-------|-------|-------|-------|
| ノード数 | 11 | 9 | 8 | 7 |
| エッジ数 | 11 | 8 | 8 | 6 |
| type種数 | 5/7 | 5/7 | **7/7** | 6/7 |
| relation種数 | 5/8 | 6/8 | 5/8 | 4/8 |
| 概要把握コメント | なし | なし | **あり** | あり |
| labelフィールド | なし | なし | **あり** | なし |

## 最重要の発見: SKILL.mdがRulesの失敗を補完

### type 7/7 達成

Rulesにmethod/problemの定義を書いたにもかかわらず、段階2では不使用（5/7）だった。段階3でSKILL.md Step 2「以下の優先順で探す: …手法…課題・障害」を読んだことで初めて出現:

- `fitness_landscape_analysis` (method) — 「フィットネスランドスケープ分析」
- `small_size_complexity_tradeoff` (problem) — 「サイズと複雑性のトレードオフ」

**語彙の定義（Rules）は効かなかったが、探索の指示（Skills）は効いた。** Geminiにとって:
- Rulesのtype定義 = 「分類の辞書」→ 「このtypeのノードを探しに行け」とは読まない
- SKILL.mdの優先順リスト = 「探索の指示」→ 「手法や課題を探す」行動を誘発

### causes の軌跡完成

| 段階 | causes件数 | 追加された制約 |
|------|-----------|--------------|
| 段階1 | 0 | なし |
| 段階2 | 2 | + Rules（causes定義が教育として効いた） |
| 段階3 | **1** | + Skills |
| 段階4 | 0 | + Hooks |

段階3ではまだ1件生存（`qt45_ribozyme → rna_self_replication`）。段階4で完全消失。**causesを殺したのはSkillsではなくHooks。** validate_yaml.shの存在がGeminiの行動を保守的にさせ、「安全な」relation（supports, produces, requires）に収束させた可能性がある。

### derives の初出現

段階1〜2で一度も使わなかったderivesが段階3で1件出現（`qt45_ribozyme → small_size_complexity_tradeoff`）。SKILL.md Step 3「派生関係: AからBが派生する（derives）」の指示が効いた。しかし段階4では再び消失。**段階3限定の出現で、Hooksで消える**——Codexと同じパターン。

## ノード構成の変化

段階2→3の変化:

| 新出現 | type | 由来 |
|--------|------|------|
| fitness_landscape_analysis | method | SKILL.md Step 2「手法」 |
| small_size_complexity_tradeoff | problem | SKILL.md Step 2「課題・障害」 |

| 消失 | type | 段階2にあった |
|------|------|--------------|
| origin_of_life | concept | 段階1から残存していた上位概念がついに消滅 |
| class_i_polymerase | entity | 比較対象 |
| structural_complexity | property | small_size_complexity_tradeoffに統合 |
| polymerase_activity | property | 消滅 |

新出現2件、消失4件で純減2。ノード数は9→8（後にさらに8→7）。SKILL.mdは「method/problemを探す」行動を誘発した一方、「上位概念や比較対象を維持する」ことには寄与しなかった。origin_of_lifeはGemini固有の抽象的ノードだったが、SKILL.mdの手順が「論文の具体的な中身」に焦点を当てたため、抽象概念が押し出された。

## SKILL.md Step遵守

| Step | 内容 | 遵守 |
|------|------|------|
| Step 1 概要把握コメント | YAMLコメントに記録 | **○（初出現）** |
| Step 2 ノード候補抽出 | 5段階の優先順 | △（method/problem出現、但し上位3段階が中心） |
| Step 3 エッジ特定 | 7観点で探す | △（5/8種。causes維持、derives新出） |
| Step 4 整合性チェック | 孤立ノード確認 | 不明（報告なし） |
| Step 5 YAML出力 | output/に出力 | ○ |

Step 1の概要把握コメントが**段階3で初めて出現**。段階1・2では出なかった。CodexはSKILL.mdなしで自発的に出していた（段階1から）。Geminiは明示的な指示があって初めて従う——この違いは「デフォルト行動の差」を反映している。

## metadata の変化

段階2: title（英語原題）, authors（文字列）, description
段階3: title（英語原題）, authors（**リスト形式**）, date, description

authorsが文字列→リスト形式に変わった。date フィールドが新たに追加（段階1・2にはなかった）。SKILL.mdに metadata のフォーマット指示はないが、SKILL.md の「構造化せよ」という全体的な方向性が、metadata のフォーマットにも波及したと推測。

## 三ツール段階3: 「段階3 = 語彙多様性のピーク」

| | Claude | Codex | Gemini |
|---|---|---|---|
| 段階3 type | 7/7 | 7/7 | **7/7** |
| 段階3 relation | 8/8 | **8/8** | 5/8 |
| 段階4 type | 7/7 | 7/7 | 6/7 (-1) |
| 段階4 relation | 8/8 | 6/8 (-2) | 4/8 (-1) |

**段階3（Rules + Skills、Hooksなし）が語彙多様性の最大点**:
- Codex: relation 段階3で8/8 → 段階4で6/8（-2）
- Gemini: type 段階3で7/7 → 段階4で6/7（-1）、causes 段階3で1件 → 段階4で0件

Claudeだけが段階3→4で多様性を維持（8/8 → 8/8、7/7 → 7/7）。Claudeの段階4で孤立ノードがHookに検出されて修正されたとき、ノード+1・エッジ+2で増える方向に動いた。**Claude にとって Hooks は「品質を上げる刺激」、Codex/Gemini にとって Hooks は「行動を保守化させる圧力」**。

この差は第2章の確率的制御と決定論的制御の相互作用の実例として極めて重要。同じ決定論的制御（validate_yaml.sh）が、モデルの傾向によって「改善」にも「委縮」にもなる。
