# Gemini CLI 段階1 — GEMINI.mdのみ

実行日: 2026-03-15
構成: GEMINI.md（6行）のみ。Rules/Skills/Hooksなし。
入力: science.adt2760.pdf（Gianni et al., Science 2026）
比較対象: chapter7/snapshots/step1/（Claude Code 段階1）、chapter9/codex/step1/（Codex CLI 段階1）

## 出力の概要

| 指標 | Gemini 段階1 | Codex 段階1 | Claude 段階1 |
|------|-------------|-------------|--------------|
| ノード数 | 11 | 16 | 22 |
| エッジ数 | 11 | 18 | 25 |
| type種数 | 5 | 7 | 9 |
| relation種数 | 5 | 7 | — (自由形式) |
| labelフィールド | なし | あり | あり |
| 概要把握コメント | なし | あり（自発） | なし |

## 粒度の勾配: 段階1の時点で既に存在

Claude 22 > Codex 16 > Gemini 11。制約なしの「素のモデル」の段階で、ノード数に2倍の差がある。つまり段階4の差（28 vs 17 vs 7）は、Rules/Skills/Hooksの効果ではなく、**モデルの基礎的な解釈傾向の差が主因**。

段階1→4の変化を並べると:

| | Claude | Codex | Gemini |
|---|---|---|---|
| 段階1（素） | 22 | 16 | 11 |
| 段階4（全部入り） | 28 | 17 | 7 |
| 変化 | +6（増加） | +1（不変） | **−4（減少）** |

Claudeは制約を足すと増える。Codexは変わらない。Geminiは制約を足すと**減る**。Geminiにとって制約は「ガイドライン」ではなく「制限」として作用した可能性がある。この仮説は段階2・3の結果で検証する。

## type の使用

Geminiが使用した5種:
- entity(3), process(3), concept(2), property(2), condition(1)

Geminiが使用しなかった2種（Codexは使用）:
- **method** — 実験手法のノードを一切抽出しなかった（de novo選択、適応度解析など）
- **problem** — 課題や障害のノードを一切抽出しなかった（鎖阻害問題など）

これはCodex/Claudeとの構造的な差異。Geminiは「論文が何を発見したか」に集中し、「どうやって発見したか」（method）と「何が障害か」（problem）を省略する傾向がある。

## relation の使用

Geminiが使用した5種:
- supports(4), produces(3), requires(2), contains(1), inhibits(1)

Geminiが使用しなかった3種（段階4でも同様に不使用だった）:
- **causes** — 因果関係が不在。段階4（全部入り）でも0件だった。段階1から一貫してcausesを使わない。
- **compares** — 比較対象ノード自体がない（class_i_polymeraseを抽出していない）
- **derives** — 派生関係がない（発見経路の中間段階を省略している）

causes不使用は段階1から一貫しており、モデルの基礎的な傾向であることが確認された。Rulesに8種を明示しても使わなかったのは「知らなかった」のではなく「使う必要を感じなかった」。

## ノードの構成

Geminiが抽出した11ノード:

| id | type | 概要 |
|----|------|------|
| qt45_ribozyme | entity | 中心分子 |
| triplet_substrates | entity | 基質 |
| class_i_polymerase | entity | 比較対象 |
| rna_templated_synthesis | process | 基盤反応 |
| self_replication | process | 自己複製 |
| spontaneous_emergence | process | 自然発生 |
| rna_world_hypothesis | concept | RNAワールド |
| origin_of_life | concept | 生命の起源 |
| eutectic_ice_environment | condition | 反応条件 |
| replication_fidelity | property | 忠実度 |
| structural_complexity | property | 構造複雑性 |

### Gemini固有のノード（Claude/Codexに存在しない）

- **origin_of_life** — 「生命の起源」を独立したconceptノードとして抽出。他の2ツールは論文の具体的な分子・反応レベルに留まるが、Geminiは論文の「意義」を上位概念としてノード化した。
- **spontaneous_emergence** — 「自然界で偶然に機能分子が生じるプロセス」。他の2ツールは size_paradox（サイズのパラドックス）として抽出した概念を、Geminiはプロセスとして再解釈。
- **structural_complexity** — 「分子構造の複雑さ」を独立propertyとして抽出。他の2ツールにはない抽象度。

### Geminiに欠落する主要概念

- 実験手法: de novo選択、in vitro進化
- 自己複製の半サイクル: 相補鎖合成、自己鎖合成（self_replicationに集約）
- 技術的障害: 鎖阻害問題
- 解決策: ヘキサマー補助基質
- 発見経路: ランダム配列プール、中間モチーフ
- 定量的結果: 忠実度94.1%、収率0.2%（数値なし）

## ネットワーク構造

6本のエッジのうち4本が `qt45_ribozyme` を source とするスター型構造。段階4（全部入り）でも同じスター型だった。制約の有無に関係なく、Geminiのネットワーク構造はスター型に収束する傾向がある。

一方で段階1には段階4にはない横接続が存在する:
- `class_i_polymerase → structural_complexity (contains)`
- `structural_complexity → spontaneous_emergence (inhibits)`
- `spontaneous_emergence → origin_of_life (requires)`
- `rna_world_hypothesis → origin_of_life (supports)`

この4本のチェーンは「大型リボザイムの複雑さ→自然発生の困難→生命の起源への示唆」という抽象的な議論の流れを表現しており、Claudeの段階1にもCodexの段階1にもない**概念レベルの推論**。Geminiは具体的な分子・反応の詳細を省略する代わりに、上位概念間の関係を構造化する傾向がある。

## metadata

最小構成: title, description の2フィールドのみ。

Codexは source_file, doi, language 等を自発的に追加。Claudeは authors, journal, year, doi を追加。Geminiは指示された最低限しか出力しない。

特筆すべきは title の書き方:
- Claude: 原題そのまま（英語）
- Codex: 原題そのまま（英語）
- Gemini: **日本語に翻訳**（「自身とその相補鎖を合成可能な小型ポリメラーゼリボザイム」）

GEMINI.mdに「日本語で記述する」とは書いていない（段階1には行動規則セクションがない）。Geminiが自発的に日本語タイトルにしたのは、プロンプトが日本語だったことへの感受性が高いためと推測される。

## 三ツール段階1の総括: 「素の解釈力」の差

段階1は「制約なしでモデルが何を出すか」のベースライン測定。結果は:

**粒度**: Claude（網羅的・22ノード） > Codex（ストーリーライン・16ノード） > Gemini（要旨+上位概念・11ノード）。この勾配は段階4と同方向であり、制約の効果ではなくモデルの基礎傾向。

**構造化のデフォルト**: Codexは訓練データからナレッジグラフの標準語彙を内在化しており、Rulesなしで7種type/7種relationを使用。Claudeは自由発明（9種type、日本語動詞句ラベル）。Geminiは部分的な標準語彙（5種type/5種relation）。

**抽象度**: Geminiは最も抽象度が高く、他の2ツールにない上位概念（origin_of_life, spontaneous_emergence）をノード化。具体的な分子・反応の詳細を省略する代わりに、概念間の推論的関係を構造化する。

**Rulesの意味がモデルごとに異なる**:
- Claudeに対して: 自由な発明を制約する → 制約の設計行為
- Codexに対して: 既存のデフォルトを確認する → 文書化行為
- Geminiに対して: 未検証（段階2で確認）→ 語彙を教えるか、さらに制限するか
