---
paths:
  - "scripts/**"
  - "output/**"
---
# ファイル配置・git ルール

## ファイル配置
- 検証・マージスクリプトは scripts/ に配置
- 最終成果物は output/ に配置

## git commit ルール
- commit メッセージは日本語で、Phase 番号を含める
  例: "Phase 2 完了: Moody論文の概念抽出"
- .env ファイル、API キーは絶対に commit しない

## アーカイブの保護
- docs/archive_*/ のファイルは読み取り専用として扱う
- 上書き・削除は禁止
