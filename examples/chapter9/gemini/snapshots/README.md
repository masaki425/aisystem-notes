# Gemini CLI 実行結果 — Claude Code・Codex CLI との比較

実行日: 2026-03-15
入力: science.adt2760.pdf（Gianni et al., Science 2026）
Geminiモデル: Gemini（gemini実行時のデフォルト）
比較対象: chapter7/output/science_adt2760.yaml（Claude Code 段階4）、chapter9/codex/output/（Codex CLI）

## 1. validate_yaml.sh 結果

| 項目 | Gemini | Codex | Claude |
|------|--------|-------|--------|
| **検証結果** | PASS | PASS | ※書式問題 |
| **ノード数** | 7 | 17 | 28 |
| **エッジ数** | 6 | 19 | 32 |
| **孤立ノード** | 0 | 0 | ※grep書式依存 |

Geminiの出力はvalidate_yaml.shの全9チェック項目をPASSした。ただし、7ノード/6エッジという極端に小さなネットワークであるため、「検証をパスしたが十分か」という問いが生じる。validate_yaml.shはノード数の下限を「1個以上」としか定義しておらず、**最小限のネットワークでも通過する**。

## 2. 三ツール比較：規模

| 指標 | Gemini | Codex | Claude | Gemini/Claude比 |
|------|--------|-------|--------|-----------------|
| ノード数 | 7 | 17 | 28 | 0.25x |
| エッジ数 | 6 | 19 | 32 | 0.19x |
| ノード/エッジ比 | 1.17 | 0.89 | 0.88 | — |
| type種使用 | 6/7 | 7/7 | 7/7 | — |
| relation種使用 | 4/8 | 6/8 | 8/8 | — |

Geminiの出力はClaudeの1/4のノード数、1/5のエッジ数。Codexの凝縮傾向（Claudeの6割）をさらに大きく下回る。**三ツールの粒度勾配: Claude（網羅）> Codex（凝縮）>> Gemini（最小限）**。

## 3. ノードの比較

### Gemini の全7ノード

| id | type | 対応するCodexノード | 対応するClaudeノード |
|----|------|---------------------|---------------------|
| `qt45_ribozyme` | entity | `qt45_ribozyme` ✓ | `qt45_ribozyme` ✓ |
| `triplet_substrates` | entity | `triplet_substrates` ✓ | `triplet_substrates` ✓ |
| `rna_self_replication` | process | `rna_self_replication` ✓ | `self_replication` ≈ |
| `rna_world_hypothesis` | concept | `rna_world_hypothesis` ✓ | `rna_world` ≈ |
| `eutectic_ice` | condition | `eutectic_ice_condition` ≈ | `eutectic_ice` ✓ |
| `high_fidelity` | property | `synthesis_fidelity_94_1` ≈ | `synthesis_fidelity` ≈ |
| `size_complexity_paradox` | problem | — | `size_paradox` ≈ |

### 三ツール共通ノード（同一ID）: **2件のみ**

`qt45_ribozyme`, `triplet_substrates`

概念的に全ツールに存在するノード（命名は異なる）: 上記7件すべて。つまりGeminiが抽出した7件は、三ツール共通の「コア概念」に相当する。

### Geminiが抽出しなかった主要概念

| 概念 | Codex | Claude | 意味 |
|------|-------|--------|------|
| de_novo_selection（発見手法） | ○ | ○ | 論文の実験方法 |
| complementary/minus_strand_synthesis | ○ | ○ | 自己複製の半サイクル |
| self/plus_strand_synthesis | ○ | ○ | 自己複製のもう半サイクル |
| strand_inhibition（鎖阻害） | ○ | ○ | 自己複製の主要障害 |
| hexamer_substrate（補助基質） | ○ | ○ | 鎖阻害の解決策 |
| class_i_polymerase（比較対象） | ○ | ○ | 既存研究との位置づけ |

Geminiは**自己複製の2つの半サイクル（相補鎖合成・自己鎖合成）を個別ノードとして抽出せず**、`rna_self_replication` 1ノードに集約した。CodexとClaudeはいずれもこの2反応を分離している。また**実験手法**（de novo選択）と**技術的障害**（鎖阻害、補助基質による解決）が丸ごと欠落している。

### type 使用分布

| type | Gemini | Codex | Claude |
|------|--------|-------|--------|
| entity | 2 | 5 | 9 |
| process | 1 | 4 | 6 |
| concept | 1 | 3 | 3 |
| property | 1 | 1 | 4 |
| condition | 1 | 1 | 1 |
| problem | 1 | 2 | 2 |
| **method** | **0** | 1 | 3 |

Geminiは `method` を一度も使わなかった。de novo選択も適応度ランドスケープ解析も抽出していないため。

## 4. エッジの比較

### relation種の使用

| relation | Gemini | Codex | Claude |
|----------|--------|-------|--------|
| supports | 2 (33%) | 9 (47%) | 5 (16%) |
| produces | 2 (33%) | 4 (21%) | 2 (6%) |
| inhibits | 1 (17%) | 3 (16%) | 4 (13%) |
| requires | 1 (17%) | 1 (5%) | 5 (16%) |
| **causes** | **0** | 1 (5%) | 6 (19%) |
| **compares** | **0** | 1 (5%) | 2 (6%) |
| **contains** | **0** | 0 | 4 (13%) |
| **derives** | **0** | 0 | 4 (13%) |
| **種数** | **4/8** | **6/8** | **8/8** |

**relation使用の勾配: Claude 8/8 > Codex 6/8 > Gemini 4/8**。

Geminiは causes, compares, contains, derives の4種を使わなかった。特に `causes`（因果関係）の不在は構造的に重要——Codexですら1件は使っており、Claudeは6件を因果で接続している。Geminiのネットワークには「AがBを引き起こす」という因果構造が存在しない。

エッジの内訳を見ると、6本中4本が `qt45_ribozyme` を source としている。ネットワーク構造がQT45を中心にした放射状（スター型）であり、概念間の横の接続がほぼない。

## 5. SKILL.md 手順の遵守

| Step | 内容 | Gemini | Codex | Claude |
|------|------|--------|-------|--------|
| Step 1 | 概要把握をYAMLコメントに記録 | ○ | ○ | ○ |
| Step 2 | ノード候補の抽出 | △（7件のみ） | ○ | ○ |
| Step 3 | エッジの特定 | △（4/8種） | ○（6/8種） | ○（8/8種） |
| Step 4 | 整合性の自己チェック | ○（孤立ノード0） | ○ | △ |
| Step 5 | YAML出力 | ○ | ○ | ○ |

Geminiは手順自体は飛ばさなかったが、Step 2のノード抽出で**優先順の1〜2（中心対象・直接の関連要素）までで止まり、3以降（比較対象・理論的枠組み・課題）からの抽出が極めて少ない**。SKILL.mdの「以下の優先順で探す」を「優先順が高いものだけ探す」と解釈した可能性がある。

## 6. metadata の差異

| フィールド | Gemini | Codex | Claude |
|-----------|--------|-------|--------|
| title | ○ | ○ | ○ |
| authors | ○ | × | ○ |
| year | ○ | × | ○ |
| source/journal | ○ (source) | ○ (source) | ○ (journal) |
| doi | × | × | ○ |
| description | ○ | ○ | ○ |

GeminiはCodexと異なりauthorsとyearを自発的に追加した。Claudeに近い振る舞い。

## 7. ファイル命名

入力: `science.adt2760.pdf`

| | Gemini | Codex | Claude |
|-|--------|-------|--------|
| 出力ファイル名 | `science.adt2760.yaml` | `science.adt2760.yaml` | `science_adt2760.yaml` |

GeminiとCodexはルール通り（リテラル）。Claudeのみドット→アンダースコア変換。

## 8. 総括：9.2 の枠組みで整理

### 解釈の傾向（一貫した方向性）

- **粒度の三段階勾配**: Claude（28ノード、網羅的） > Codex（17ノード、主要ストーリーライン） >> Gemini（7ノード、論文の要旨レベル）。Geminiは論文のAbstractに書かれている程度の概念のみ抽出し、本文の詳細に踏み込んでいない。
- **ネットワーク構造**: Geminiはスター型（QT45を中心に放射）。Codexはやや線形（発見→機構→検証の流れ）。Claudeはメッシュ型（概念間の横接続が豊富）。
- **抽象度**: Geminiは最も抽象度が高い。`high_fidelity`（高忠実度複製）というノードは具体的数値（94.1%）をlabelではなくdescriptionに持ち、概念として抽象化している。Codexは`synthesis_fidelity_94_1`とIDに数値を埋め込み、Claudeは`synthesis_fidelity`としてdescriptionに範囲（92.6〜94.1%）を記載。

### 解釈の癖（予測しにくい反応）

- **causes の不使用**: 8種のrelationリストが明示されているにもかかわらず、causesを一度も使わなかった。因果関係を「produces」や「supports」に読み替えている。例: 「QT45が自己複製を実現する」をcausesではなくproducesとした。
- **method type の不使用**: de novo選択など実験手法のノードを一切抽出しなかった。論文の実験的側面よりも概念的側面を優先する傾向。
- **SKILL.md Step 2 の縮小解釈**: 「以下の優先順で探す」の5段階を網羅せず、上位1〜2段階で停止。指示の「探す」を「全部探す」ではなく「重要なものを探す」と解釈した。

### 感受性の差

- **Step 1（概要把握）**: 三ツールとも正確に遵守。SKILL.md冒頭の「手順を飛ばさず」と Step 1 の明確な指示が全モデルで効いている。
- **type制約**: Gemini 6/7、Codex 7/7、Claude 7/7。Geminiのみmethodを使用しなかったが、これはmethodノードを抽出しなかった結果であり、禁止typeを使ったわけではない。制約の「使わない」方向は守られた。
- **relation制約**: Gemini 4/8、Codex 6/8、Claude 8/8。Rulesの「これ以外は使わない」（禁止方向）は三ツールとも完全遵守。しかし「使え」方向の網羅性はモデルの解釈に委ねられており、Geminiが最も低い。

## 9. 三ツール横断の発見

### validate_yaml.sh の構造的限界

三ツールの比較から、validate_yaml.shの設計に2つの限界が明らかになった：

1. **書式依存性**（Codexテストで発見）: grepパターンがYAMLの等価な書式を区別する。
2. **品質下限の不在**（Geminiテストで発見）: ノード7個・エッジ6個でも全チェック項目をPASSする。45塩基のリボザイムの構造化に7ノードで「十分か」は、スクリプトでは判定できない。**最小限の妥当性（well-formedness）は検証できるが、十分性（adequacy）は検証できない**。

これは第2章の「決定論的制御の射程」の実例。Hooksで強制できるのは形式的な整合性であり、概念的な十分性の判断は確率的制御（モデルの判断）に委ねるしかない。あるいは、ノード数の下限（例: 15以上）をvalidate_yaml.shに追加するという対処も考えられるが、それは「何ノードが適切か」という判断を人間がスクリプトにハードコードすることになり、タスクの汎用性を失う。

### 粒度勾配の解釈

三ツールの粒度勾配（Claude 28 > Codex 17 > Gemini 7）は、9.2で述べた「解釈の傾向」の最も明確な実例。同じ論文、同じSKILL.md、同じRulesを渡して、出力の規模が4倍異なる。

ただし、これは「Claudeが正しくGeminiが間違い」ではない。用途による。論文の要旨を構造化したいならGeminiの7ノードで十分かもしれない。概念間の詳細な関係を分析したいならClaudeの28ノードが必要。**「何ノードが適切か」はproposal.mdで明示すべき要件**であり、今回のHarnessにはこの指定がなかった。
