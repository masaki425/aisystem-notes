# Codex CLI 実行結果 — Claude Code との比較

実行日: 2026-03-15
入力: science.adt2760.pdf（Gianni et al., Science 2026）
Codexモデル: GPT系（codex実行時のデフォルト）
比較対象: chapter7/output/science_adt2760.yaml（Claude Code 段階4出力）

## 1. validate_yaml.sh 結果

| 項目 | Codex | Claude |
|------|-------|--------|
| **検証結果** | PASS | ※後述 |
| **ノード数** | 17 | 28 |
| **エッジ数** | 19 | 32 |
| **孤立ノード** | 0 | ※後述 |

**※ Claudeの検証結果について**: chapter7/output/ に保存されている最終YAMLは、エッジの書式（`  - source:` vs `    source:`）がvalidate_yaml.shのgrep パターンと合致せず、スクリプト上は6件の孤立ノードとして検出される。これはYAML としては等価だが、validate_yaml.sh がYAMLパーサではなくgrep ベースである脆さに起因する。Codex出力は各エッジを `  -` と `    source:` の2行に分けて書いており、grepパターンに適合した。**検証スクリプトの書式依存性**自体が、移植テストで発見された問題の一つ。

## 2. ノードの比較

### 数量

| 指標 | Codex | Claude | 差異 |
|------|-------|--------|------|
| ノード総数 | 17 | 28 | Claude が 1.6倍 |
| concept | 3 | 3 | 同数 |
| entity | 5 | 9 | Claude が 1.8倍 |
| process | 4 | 6 | Claude が 1.5倍 |
| property | 1 | 4 | Claude が 4倍 |
| method | 1 | 3 | Claude が 3倍 |
| condition | 1 | 1 | 同数 |
| problem | 2 | 2 | 同数 |
| **type種使用** | **7/7** | **7/7** | 両方フルカバー |

### ID命名の一致

完全一致ノード（同一ID）: **4件のみ**
- `qt45_ribozyme`, `de_novo_selection`, `rna_templated_rna_synthesis`, `triplet_substrates`

概念的に対応するが命名が異なるノード: **11組**

| Codex | Claude | 命名の差異 |
|-------|--------|-----------|
| `complementary_strand_synthesis` | `minus_strand_synthesis` | 機能名 vs 生化学名 |
| `self_strand_synthesis` | `plus_strand_synthesis` | 機能名 vs 生化学名 |
| `rna_self_replication` | `self_replication` | 接頭辞の有無 |
| `rna_world_hypothesis` | `rna_world` | 「仮説」の付与 |
| `eutectic_ice_condition` | `eutectic_ice` | 「条件」の付与 |
| `random_rna_pool` | `random_sequence_pool` | rna vs sequence |
| `auugau_hexamer` | `hexamer_substrate` | 具体配列名 vs 一般名 |
| `strand_duplex_inhibition` | `strand_inhibition` | duplex の有無 |
| `synthesis_fidelity_94_1` | `synthesis_fidelity` | 数値の埋め込み |
| `triplet_binding_equilibrium` | `folding_equilibrium` | binding vs folding |
| `class_i_polymerase_5tu` | `class_i_polymerase` + `five_tu_ribozyme` | 1ノード vs 2ノード分離 |

**観察**: Codexは「何をする概念か」（機能名）で命名する傾向。Claudeは「生化学での呼称」（専門用語）で命名する傾向。Codexは数値やサフィックスをIDに含める（`synthesis_fidelity_94_1`）。

### Claude のみに存在するノード（12件）

理論的枠組み: `eigen_error_threshold`, `quasispecies`
中間段階: `qt51_ribozyme`, `three_motifs`（発見経路の詳細）
手法の詳細: `fitness_landscape_analysis`, `ph_freeze_thaw_cycles`
分子の性質: `trans_activity`, `regiospecificity`, `ribozyme_abundance`
機能実証: `hammerhead_ribozyme`
プロセス: `rna_recombination`
問題提起: `size_paradox`

### Codex のみに存在するノード（2件）

`small_motif_abundance_hypothesis` — Claude の `ribozyme_abundance`（property）と概念的に近いが、Codex は「仮説」（concept）として抽出。
`low_yield_problem` — Claude は低収率を明示的なノードとしていない（descriptionに記述はある）。

## 3. エッジの比較

### relation種の使用

| relation | Codex | Claude |
|----------|-------|--------|
| supports | 9 (47%) | 5 (16%) |
| produces | 4 (21%) | 2 (6%) |
| inhibits | 3 (16%) | 4 (13%) |
| causes | 1 (5%) | 6 (19%) |
| requires | 1 (5%) | 5 (16%) |
| compares | 1 (5%) | 2 (6%) |
| **contains** | **0** | 4 (13%) |
| **derives** | **0** | 4 (13%) |
| **種数** | **6/8** | **8/8** |

**観察**: Codex は `contains`（構成関係）と `derives`（派生関係）を一度も使わなかった。特に `derives` の不在は構造的に重要——Claude は `three_motifs → qt51_ribozyme → qt45_ribozyme` という発見経路を derives チェーンで表現したが、Codex は `de_novo_selection → qt45_ribozyme` と直接 produces で接続し、中間段階を省略した。

Codex は `supports` に偏重（47%）。これは 9.2 で述べた「解釈の傾向」に該当する——Codex（GPT系）は概念間の支持・裏付け関係を優先的に抽出する傾向がある。

## 4. metadata の差異

| フィールド | Codex | Claude |
|-----------|-------|--------|
| title | ○ | ○ |
| source | ○ | × |
| description | ○ | ○ |
| authors | × | ○ |
| journal | × | ○ |
| year | × | ○ |
| doi | × | ○ |

Rules に metadata の必須フィールドは `metadata, nodes, edges の3セクションを必ず含める` としか定義していないため、どちらもルール違反ではない。ただし Claude は書誌情報を自発的に追加した。

## 5. SKILL.md 手順の遵守

| Step | 内容 | Codex | Claude |
|------|------|-------|--------|
| Step 1 | 概要把握をYAMLコメントに記録 | ○ | ○ |
| Step 2 | ノード候補の抽出 | ○ | ○ |
| Step 3 | エッジの特定 | ○（6/8種） | ○（8/8種） |
| Step 4 | 整合性の自己チェック | ○（孤立ノード0） | △（※書式問題で判定不可） |
| Step 5 | YAML出力 | ○ | ○ |

## 6. ファイル命名の差異

入力: `science.adt2760.pdf`
Rules: 「入力ファイル名から拡張子を除いたもの」

| | Codex | Claude |
|-|-------|--------|
| 出力ファイル名 | `science.adt2760.yaml` | `science_adt2760.yaml` |
| 解釈 | ルール通り（リテラル） | ドット→アンダースコア変換 |

Codex はルールを字義通り適用。Claude はファイル名中のドットをアンダースコアに変換した。これも 9.2 の「解釈の癖」の一例。

## 7. 総括：9.2 の枠組みで整理

### 解釈の傾向（一貫した方向性）

- **粒度**: Codex は凝縮（17ノード）、Claude は網羅（28ノード）。Claude は理論的枠組み（アイゲン閾値、準種）、発見の中間段階（3モチーフ→QT51→QT45）、分子の性質（トランス活性、位置特異性）まで展開する。Codex は論文の主要ストーリーラインに集中する。
- **関係の選好**: Codex は supports 偏重（47%）。Claude は 8 種を均等に使い、特に derives/contains で階層構造を表現する。
- **命名**: Codex は機能的・記述的（`complementary_strand_synthesis`）。Claude は生化学専門用語寄り（`minus_strand_synthesis`）。

### 解釈の癖（予測しにくい反応）

- **relation の欠落**: Codex は contains と derives を使用しなかった。8種のリストが Rules に明示されているにもかかわらず。
- **ファイル名変換**: Claude がドットをアンダースコアに変換した。ルールのリテラルな解釈と異なる。
- **metadata の自発的拡張**: Claude が書誌情報を追加した。指示にないが「あるべき」と判断した。

### 感受性の差

- **概要把握**: 両者とも Step 1 の指示に従い YAML コメントとして記録。SKILL.md 冒頭の「手順を飛ばさず、順番通りに実行すること」が効いている。
- **type/relation 制約**: type は両者とも 7/7 で完全遵守。relation は Claude 8/8、Codex 6/8。Rules での制約指示（「これ以外は使わない」）の「使え」方向の強制力は relation の方が弱い。

## 8. validate_yaml.sh の書式依存性問題

本テストで発見された問題として、validate_yaml.sh の grep パターンが YAML の等価な書式バリエーションを正しく処理できないことが判明した。

```yaml
# Codex の書式（grepパターンに適合）
edges:
  -
    source: node_a
    target: node_b
    relation: causes

# Claude の書式（grepパターンに不適合）
edges:
  - source: node_a
    target: node_b
    relation: causes
```

両者はYAMLとして等価だが、`grep "    source:"` は前者のみに一致する。決定論的検証スクリプトが「YAMLパーサではなくテキストパターンマッチ」で実装されていたことで、モデル間の書式の差異に対して脆弱だった。修正案: `yq` や Python の PyYAML を使ったパース方式への書き換え。
