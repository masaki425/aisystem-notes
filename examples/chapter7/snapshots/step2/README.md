# Step 2: Rulesを追加して構造化を実行

## 目的

Step 1のCLAUDE.mdに加えて、`.claude/rules/structurize.md`を追加し、フォーマットの不安定さが解消されるかを観察する。

## 追加したファイル

### .claude/rules/structurize.md

```markdown
# 構造化ルール

## ノードのルール
- id は snake_case で命名する
- type は以下の7種から選択する。これ以外のtypeは使わない
  - concept, entity, process, property, method, condition, problem

## エッジのルール
- relation は以下の8種から選択する。これ以外のrelationは使わない
  - causes, requires, produces, supports, inhibits, contains, compares, derives
- label は不要（relationで関係を表現する）

## YAML出力のルール
- metadata, nodes, edges の3セクションを必ず含める
- description は1〜2文で簡潔に書く
- 日本語で記述する
```

### Claude Codeへの指示

```
/clear してからセッション再開
input/の論文を読んで、概念ネットワークのノードとエッジを抽出してYAMLにして
```

## 出力の概要

- **ファイル**: `output/science_adt2760.yaml`
- **ノード数**: 27（Step 1: 22）
- **エッジ数**: 30（Step 1: 25）

---

## Rulesの遵守状況（詳細検証）

### ノードtype: 全27ノードが7種に準拠 ✅

| type | ノード数 | 具体例 |
|------|---------|--------|
| concept | 3 | rna_world, eigen_error_threshold, quasispecies |
| entity | 9 | qt45_ribozyme, triplet_substrates, hexamer_substrate, random_sequence_pool 等 |
| process | 5 | self_replication, minus_strand_synthesis, folding_equilibrium 等 |
| property | 4 | synthesis_fidelity, trans_activity, regiospecificity, ribozyme_abundance |
| method | 3 | de_novo_selection, fitness_landscape_analysis, ph_freeze_thaw_cycles |
| condition | 1 | eutectic_ice |
| problem | 2 | strand_inhibition, size_paradox |

Rules外のtype（Step 1で使われていた molecule, theory, analysis, context）は出現しなかった。

### エッジrelation: 全30エッジが8種に準拠 ✅

| relation | エッジ数 | 具体例 |
|----------|---------|--------|
| causes | 5 | qt45→rna_templated_rna_synthesis, eutectic_ice→qt45 等 |
| requires | 4 | minus_strand_synthesis→self_replication, rna_templated_rna_synthesis→triplet_substrates 等 |
| produces | 2 | de_novo_selection→three_motifs, qt45→hammerhead_ribozyme |
| supports | 4 | self_replication→rna_world, fitness_landscape_analysis→qt45 等 |
| inhibits | 4 | strand_inhibition→self_replication, qt45→size_paradox 等 |
| contains | 4 | five_tu→class_i_polymerase, qt45→trans_activity 等 |
| compares | 2 | qt45↔class_i_polymerase, qt45↔five_tu |
| derives | 4 | three_motifs→qt51, synthesis_fidelity→eigen_error_threshold 等 |

Step 1の自由な日本語ラベル（「が触媒」「を支持」「の性質」等）は完全に消え、labelフィールド自体が出力されなかった。

### ID命名: 全ノードがsnake_case ✅

Step 1で `qt45`, `five_tu`, `ph_freeze_thaw` だったIDが、Step 2では `qt45_ribozyme`, `five_tu_ribozyme`, `ph_freeze_thaw_cycles` とより記述的になった。全IDが `[a-z0-9_]+` パターンに合致。

### YAML出力ルール ✅

- metadata, nodes, edges の3セクション: 存在する
- descriptionの長さ: 全ノード・全エッジが1〜2文（最長で `qt45_ribozyme` の2文）
- 言語: 日本語で記述されている

### エッジ参照の整合性（Rulesでは未規定だが確認）

全30エッジのsource/targetが、27ノードのIDのいずれかを参照しているかを目視確認した。

- **孤立エッジ（存在しないIDへの参照）**: 0件 ✅
- **孤立ノード（どのエッジにも参照されないノード）**: `ribozyme_abundance` のみ。ノードとして存在するがどのエッジからも参照されていない。これ自体はエラーではないが、ネットワークとしては浮いている。

### relation の意味的妥当性（borderlineなケース）

Rulesに準拠したrelation typeが選ばれているが、意味的に議論の余地があるエッジがいくつかある:

1. **`qt45_ribozyme → size_paradox` (inhibits)**: QT45がサイズのパラドックスを「阻害する」という表現。意味的には「解消する」「反証する」に近いが、8種の選択肢にそのようなrelationがないため inhibits が選ばれた。Rulesの選択肢が概念の表現を制約している例。

2. **`five_tu_ribozyme → class_i_polymerase` (contains)**: 5TUがクラスIに「含まれる」という関係。実際には「属する」であり、containsの定義（AがBを含む）とは方向が逆。8種のrelationに「belongs_to」や「is_a」がないため、containsで代用された。

3. **`synthesis_fidelity → eigen_error_threshold` (derives)**: 忠実度がアイゲン閾値に「派生する」という表現。実際には「忠実度がアイゲン閾値の条件を規定する」であり、derives（AからBが派生する）とは意味が異なる。

これらは「Rulesの選択肢が限定的すぎる」のか「8種で十分で、表現を工夫すればよい」のかは設計判断の問題。第8章で3本に拡張する際に、relation typeの追加が必要になるかもしれない。

---

## Step 1との比較

### 改善された点（Rulesの効果）

1. **ノードtypeが統一された**: Step 1の9種（AIが自由発明）→ Rulesで定義した7種に完全準拠。再実行しても同じtype体系が使われる見込みが高い。

2. **エッジrelationが統一された**: Step 1の自由な日本語動詞句 → 定義済み8種に完全準拠。「が触媒」も「を支持」も「の性質」も消え、構造化されたrelation typeに統一された。

3. **ID命名が記述的になった**: `qt45` → `qt45_ribozyme`、`five_tu` → `five_tu_ribozyme` のように、IDだけで何を指しているか推測しやすくなった。

4. **descriptionが簡潔になった**: Step 1では複数文にわたる長い説明（最長5行）があったが、Step 2では1〜2文に収まっている。

### 変化した点（Rulesの効果ではなく、実行ごとの揺れ）

1. **ノード数が増えた（22→27）**: Step 1にはなかった概念が6つ新たに出現:
   - `random_sequence_pool`: 実験の入力素材
   - `rna_templated_rna_synthesis`: QT45の触媒する反応の上位概念
   - `folding_equilibrium`: QT45の二面的な性質（触媒型/鋳型型）
   - `rna_recombination`: 進化を加速する副次的メカニズム
   - `ribozyme_abundance`: 配列空間における出現頻度
   - `size_paradox`: 論文が解決した根本的問題

   これらはRules追加によって抽出されたのではなく、LLMの確率的な読解の揺れ。同じRulesでもう一度実行したら、異なるノード集合になる可能性がある。

2. **ノードの粒度が変わった**: Step 1では `qt_ribozyme`（QTリボザイム一般）と `qt45`（特定バリアント）が別ノードだったが、Step 2では `qt45_ribozyme` に集約された。粒度の判断基準がRulesに定義されていないため、AIの裁量に委ねられている。

### Rulesが効かなかった領域（確率的制御の限界）

1. **抽出の手順**: ノードとエッジをどの順序で、どんな基準で抽出するかはRulesでは制御できない。Step 1とStep 2でノード構成が異なるのがその証拠。Rulesはフォーマットを固定するが、内容は固定しない。

2. **ノード粒度の判断**: 「QT45の性質（fidelity, trans_activity等）を独立ノードにするか、属性にするか」はRulesでは制御されていない。Step 2では独立ノード + containsエッジで表現されたが、別の実行ではエッジの属性として埋め込まれるかもしれない。

3. **ノード数・エッジ数**: Rulesには「ノード数の目安」「エッジ数の目安」が定義されていないため、抽出の網羅性はAIの判断に依存する。

### 今回守られたが、保証はない点

今回の実行ではRulesは100%遵守された。しかし、これは**保証された結果ではなく、確率的に高い遵守率が実現した結果**にすぎない。具体的には:

- 今回はtype 7種に完全準拠したが、別の実行でAIが「このノードは7種のどれにも当てはまらない」と判断すれば、Rules外のtypeを生成する可能性がある
- 今回はlabelフィールドが完全に消えたが、AIが「関係の補足説明が必要」と判断すればlabelを追加する可能性がある
- 今回はdescriptionが1〜2文だったが、複雑な概念に対してAIが「2文では説明しきれない」と判断すれば長くなる可能性がある

Rulesは「守る確率が高い指示」であり、「必ず守られる制約」ではない。この違いが、Step 4のHooks（決定論的制御）が必要になる理由である。

---

## Step 3への課題

Step 2で「フォーマット」は安定した。しかし「何を抽出するか」「どの順序で抽出するか」はまだAI任せであり、実行ごとにノード構成が変わりうる。次にSkillsで「手順」を標準化する。具体的には、論文を読む→主要概念を抽出→関係を特定→YAML出力、という手順を定義し、抽出の粒度と順序を安定させる。
