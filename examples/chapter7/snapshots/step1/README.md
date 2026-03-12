# Step 1: CLAUDE.mdのみで構造化を実行

## 目的

Harness機能を何も追加せず、CLAUDE.md（6行）だけでAIに論文の構造化を依頼したとき、何が起きるかを観察する。

## 入力

### 論文
- **ファイル**: `input/science.adt2760.pdf`
- **論文**: Gianni et al., "A small polymerase ribozyme that can synthesize itself and its complementary strand", Science (2026)
- **内容**: in vitro進化で発見された約45ヌクレオチドの小型RNAポリメラーゼリボザイム（QT45）が、自身の(+)鎖と(-)鎖の両方を合成可能であることを実証。RNA World仮説を支持する成果。

### CLAUDE.md（全文）

```markdown
# 論文構造化プロジェクト

input/ にある論文PDFを読み、概念ネットワークの構成要素（ノードとエッジ）を抽出してYAMLファイルに出力する。

## ディレクトリ構成
- input/    — 論文PDF
- output/   — 生成されるYAMLファイル
```

### Claude Codeへの指示

```
input/の論文を読んで、概念ネットワークのノードとエッジを抽出してYAMLにして
```

## 出力

- **ファイル**: `output/science_adt2760.yaml`
- **ノード数**: 22
- **エッジ数**: 25
- **ノードtype**: molecule, theory, process, property, method, condition, analysis, context, problem（9種類）

### 出力の構造

```yaml
metadata:
  title: "..."
  authors: [...]
  journal: Science
  year: 2026

nodes:
  - id: qt45
    label: QT45リボザイム
    type: molecule
    description: >
      QTリボザイムの最適化バリアント...

edges:
  - source: qt45
    target: minus_strand_synthesis
    label: が触媒
    description: QT45が自身を鋳型として(-)鎖合成を触媒
```

## 観察結果

### うまくいった点（確率的制御の強み）

- CLAUDE.md 6行だけで、論文の主要概念が網羅的に抽出された
- ノード間の関係（因果、比較、支持）が概ね正しく捉えられている
- YAML形式で出力され、機械可読な構造になっている
- 論文のドメイン知識がなくても、構造化された出力が得られた

### 不安定な点（次のステップで解決すべき問題）

1. **ノードtypeが自由発明**: molecule, theory, process, property, method, condition, analysis, context, problem の9種類。定義されたリストからの選択ではなく、AIが自由に命名した。次回実行時に異なるtype体系になる可能性がある。

2. **エッジのlabelが不統一**: 「が触媒」「を支持」「の性質」「から発見」「より遥かに小型」など、日本語動詞句で書かれているが、統一されたrelation typeの定義がない。同じ関係が異なるlabelで表現されうる。

3. **ID命名規則が未定義**: `qt45`, `qt_ribozyme`, `minus_strand_synthesis`, `ph_freeze_thaw` — snake_caseで書かれているが、明示的なルールはない。次回は異なる命名になりうる。

4. **weightやスコアがない**: エッジの重要度を判断する手段がない。すべてのエッジが等価に見える。

5. **再現性がない**: 同じ指示を再度実行したら、ノード数・type体系・エッジ構成が変わる可能性が高い。

## Step 2への課題

Step 1で見えた不安定さのうち、**フォーマットの問題**（type体系、relation type、ID命名規則）をRulesで解決する。Rulesは「やってはいけないこと」「守るべきフォーマット」を定義する確率的制御で、CLAUDE.mdよりも具体的な行動規則を提供する。
