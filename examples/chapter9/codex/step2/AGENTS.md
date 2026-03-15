# 論文構造化プロジェクト

input/ にある論文PDFを読み、概念ネットワークの構成要素（ノードとエッジ）を抽出してYAMLファイルに出力する。

## ディレクトリ構成
- input/    — 論文PDF
- output/   — 生成されるYAMLファイル

## 行動規則

### ノードのルール
- id は snake_case で命名する（例: `qt45_ribozyme`, `rna_world`）
- type は以下の7種から選択する。これ以外のtypeは使わない
  - concept: 理論・仮説・抽象概念
  - entity: 分子・物質・具体的な存在
  - process: 反応・変換・プロセス
  - property: 性質・特性・測定値
  - method: 手法・技術・実験手順
  - condition: 環境条件・制約
  - problem: 課題・障害・未解決問題

### エッジのルール
- relation は以下の8種から選択する。これ以外のrelationは使わない
  - causes: AがBを引き起こす
  - requires: BがAを必要とする
  - produces: AがBを生成する
  - supports: AがBを支持・裏付ける
  - inhibits: AがBを阻害する
  - contains: AがBを含む・構成する
  - compares: AとBが比較される
  - derives: AからBが派生する
- label は不要（relationで関係を表現する）

### YAML出力のルール
- ファイル名は `output/{入力ファイル名から拡張子を除いたもの}.yaml` とする
- metadata, nodes, edges の3セクションを必ず含める
- description は1〜2文で簡潔に書く
- 日本語で記述する
