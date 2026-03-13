# Task Config

## プロジェクトパス

base: .

## 入力

| ラベル | パス | 説明 |
|--------|------|------|
| Gianni論文 | input/science.adt2760.pdf | QT45リボザイムによるRNA自己複製（第7章でも使用） |
| Moody論文 | input/s41559-024-02461-1.pdf | LUCAのゲノム再構成と年代推定 |
| Yarus論文 | input/s00239-009-9270-1.pdf | 遺伝暗号の起源と立体化学仮説 |

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
| スキーマ参照 | docs/spec.md のスキーマ定義セクション |

## 規約

- 言語: 日本語（ノードのlabel、description）
- ファイル命名規則: 論文のfirst authorの姓（小文字）
- その他: 専門用語は英語のまま使用可

## メモ

- 第8章の反復サイクルデモ用プロジェクト
