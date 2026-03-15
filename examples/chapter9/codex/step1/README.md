# Codex CLI 段階1 — AGENTS.mdのみ

実行日: 2026-03-15
構成: AGENTS.md（6行）のみ。Rules/Skills/Hooksなし。
入力: science.adt2760.pdf（Gianni et al., Science 2026）
比較対象: chapter7/snapshots/step1/（Claude Code 段階1）

## 出力の概要

| 指標 | Codex 段階1 | Claude 段階1 | Gemini 段階1 |
|------|-------------|-------------|--------------|
| ノード数 | 16 | 22 | 11 |
| エッジ数 | 18 | 25 | 11 |
| type種数 | 7 | 9 | 5 |
| type命名 | 定義済み語彙と一致 | 自由発明 | 定義済み語彙の部分集合 |
| relation/label | 7種の定義済み語彙 | 自由な日本語動詞句 | 5種の定義済み語彙 |
| labelフィールド | あり（日本語） | あり（日本語） | なし |
| 概要把握コメント | あり（自発的） | なし | なし |

## 最重要の発見: Codexの「デフォルト語彙」

段階1にはRulesが存在しない。type体系もrelation体系もどこにも定義されていない。にもかかわらず、Codexの出力は段階2で導入するRulesの語彙と**完全に一致**する。

使用されたtype 7種:
- entity, process, property, method, condition, concept, problem
- これは段階2のRulesに定義する7種と**全く同じ**

使用されたrelation 7種:
- produces(5), supports(4), causes(3), derives(2), inhibits(2), requires(1), contains(1)
- 段階2のRulesに定義する8種のうちcomparesを除く7種

さらに「## 概要把握」コメントをYAML冒頭に自発的に記載している。これは段階3で導入するSKILL.mdのStep 1に定義する出力要件と一致する。SKILL.mdは存在しないのに。

## 解釈

GPTはナレッジグラフ構築のパターンを訓練データから内在化しており、entity/concept/process等のtype体系やcauses/supports/inhibits等のrelation体系を「デフォルトの語彙」として持っている。我々がRulesに書いた7種/8種は知識表現分野の標準的語彙であり、GPTの訓練データに大量に含まれている。

これは重要な帰結をもたらす:
- **Codexに対してRulesを書くことは「制約を加える」のではなく「既に持っているデフォルトを確認する」行為**である可能性が高い
- 段階1→4でCodexのノード数がほぼ不変（16→17）だった理由がここで説明できる——最初から「完成形に近い出力」を出しており、Rules/Skillsを足しても変わらない

## Claude段階1との対比

Claudeは段階1で9種の自由typeを発明した（molecule, theory, analysis, context等）。Rulesが「ないとき」の振る舞いが根本的に異なる:
- **Claude**: 制約がなければ自由に発明する → Rulesは「制約を加える設計行為」
- **Codex**: 制約がなくてもデフォルト語彙で構造化する → Rulesは「デフォルトを確認する文書化行為」

同じ「Rulesを書く」が、モデルとの関係によって異なる機能を持つ。

## ノードの構成

Codexが抽出した16ノード:

| id | type | 概要 |
|----|------|------|
| qt45_ribozyme | entity | 中心分子 |
| random_rna_sequence_pool | entity | 出発点 |
| triplet_substrates | entity | 基質 |
| plus_minus_duplex | entity | 阻害因子 |
| pppauugau_hexamer | entity | 補助基質 |
| in_vitro_selection | method | 発見手法 |
| eutectic_ice_condition | condition | 反応条件 |
| rna_templated_rna_synthesis | process | 基盤反応 |
| complementary_strand_synthesis | process | (-)鎖合成 |
| plus_strand_self_synthesis | process | (+)鎖合成 |
| functional_ribozyme_synthesis | process | 機能性RNA合成 |
| small_size_45nt | property | 小型性 |
| copying_fidelity_94_1 | property | 忠実度 |
| low_yield_around_0_2 | property | 低収率 |
| strand_inhibition_problem | problem | 鎖阻害 |
| rna_world_hypothesis | concept | RNAワールド |

Claudeの22ノードと比べて、以下が欠落:
- 理論的枠組み: アイゲン閾値、準種、プレバイオティック化学
- 発見経路の中間段階: 3モチーフ、QT51
- 分子の性質: トランス活性、位置特異性
- 比較対象の詳細: クラスIポリメラーゼ、5TU

逆にCodexのみに存在: low_yield_around_0_2（低収率問題を独立ノード化）、plus_minus_duplex（二本鎖を独立entityとして抽出）

## metadataの自発的拡張

Codexは以下のフィールドを自発的に追加:
- source_file, output_file（ファイルパス）
- doi（論文識別子）
- language: "ja"

Claudeは authors(8名), journal, year, doi を追加。Codexはファイルのメタ情報を重視し、Claudeは書誌情報を重視——モデルの「何が重要か」の判断が異なる。
