# Task Config

## プロジェクトパス

base: .

## 入力

| ラベル | パス | 説明 |
|--------|------|------|
| Gianni論文 | input/science.adt2760.pdf | QT45リボザイムによるRNA自己複製（Science 2026） |
| Moody論文 | input/s41559-024-02461-1.pdf | LUCAのゲノム再構成と年代推定（Nature Ecology & Evolution 2024） |
| Yarus論文 | input/s00239-009-9270-1.pdf | 遺伝暗号の起源と立体化学仮説（J Mol Evol 2009） |

## 出力

| ラベル | パス | 形式 |
|--------|------|------|
| Gianni個別YAML | output/gianni.yaml | YAML |
| Moody個別YAML | output/moody.yaml | YAML |
| Yarus個別YAML | output/yarus.yaml | YAML |
| 統合YAML | output/merged.yaml | YAML |

## テンプレート

| 用途 | パス |
|------|------|
| スキーマ参照 | examples/chapter7/output/science_adt2760.yaml |

## 規約

- 言語: 日本語（label、description）
- ファイル命名規則: 論文のfirst authorの姓（小文字）
- ノードID命名規則: snake_case、英語表記、seed list優先
- その他: なし

## メモ

- 第8章のデモ用プロジェクト
- サイクル2: seed list追加による命名揺れ対策
