# 概念ネットワーク統合プロジェクト

## 概要
生命の起源に関する論文3本から概念ネットワークを個別に抽出し、統合された概念ネットワーク（YAML）を構築する。第8章のデモとして使用。

## 技術スタック
- Python 3.x（検証スクリプト、マージスクリプト）
- PyYAML（YAML解析）

## 実行方法（Claude Code）

### 開発系
- `/setup` - proposal.md → spec.md + ファイル一式を一括生成（初回のみ）
- `/design-review` - 設計確認（Claude Code・実装前・任意）
- `/design-review codex` - 設計確認（Codex CLI・より詳細な分析）
- `/execute` - 実装（メイン）
- `/result-review` - 結果確認 + 修正提案（Claude Code）
- `/result-review codex` - Codex でレビュー → issues.md 記録 → 修正提案

### GitHub 系
- `/sync` - GitHub から最新の変更を取り込む（作業開始前）
- `/publish` - GitHub にアップロード（作業完了後）
- `/release` - バージョンタグ + GitHub Release 作成（節目で）

## 作業ルール
- 共同開発時は作業開始前に `/sync` を実行すること
- 詳細なルールは `.claude/rules/` を参照

## 並列 Worker 実行ルール（v19・エージェントモード）
- Phase 1〜3の Worker（worker_gianni, worker_moody, worker_yarus）は **必ず Taskツールで同時起動** すること
- Taskツールは最大 10 個まで同時起動可能
- 逐次起動（一つずつ順番に起動）は禁止
- Worker の起動方法: Taskツールの prompt に `.claude/agents/{agent_id}.md` の内容を含めること

## 仕様書の更新
Project のチャットで依頼するか、Claude Code で直接指示：
「.claude/workflow-template.md を参照して、spec.md を更新して」

## 参照ファイル
- proposal.md（提案書: 全工程のインプット定義）
- docs/task_config.md（環境設定: パス・規約）
- docs/spec.md（仕様書: 目的 + 実装方針 + 自動検証 + エージェント定義）
- docs/progress.md（進捗管理）
- logs/issues.md（発見した問題）
- logs/agent_log.md（エージェント実行ログ）
- .claude/commands/（実行ワークフロー）
- .claude/rules/（ガイドライン）
- .claude/agents/（Worker エージェント定義）
- .claude/settings.json（Hooks 定義）
