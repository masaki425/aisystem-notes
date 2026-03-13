spec.md のタスクを実行する。
【読み込み】→【モード判定】→【実行】→【完了処理】の順に全て実行する。
完了処理まで到達するか、blocked で明示的に停止するまで、途中で止まらない。

※ 詳細なルール・禁止事項は .claude/rules/ を参照
※ progress.md 更新と git commit は Hooks（.claude/settings.json）で強制チェックされる
※ Phase 完了時の自動検証は spec.md の「自動検証」セクションを参照
※ Phase 完了時の自動レビューは spec.md の「自動レビュー基準」セクションを参照

【読み込み】
以下を全て読んでから次に進む:
1. docs/progress.md（状態確認）
2. docs/spec.md（目的・成功基準・タスク確認）
3. docs/task_config.md（存在する場合）
4. CLAUDE.md（初回のみ）

【git 初期化確認（全モード共通）】
.git が存在しない場合は以下を実行する（/setup で未実行の可能性があるため）:
  a. git init
  b. .gitignore がなければ作成（data/, output/ を除外。logs/ は除外しない）
  c. git add . && git commit -m "initial setup"
  d. 「⚠️ git が未初期化だったため、初期化しました」と報告

【モード判定】
spec.md に「エージェント定義」セクションがあるか確認:
■ あり → 【エージェントモード】へ

=== 【エージェントモード】 ===

Lead エージェントとして Worker を順番に起動・管理する。

0. logs/agent_log.md が存在しない場合は作成する

1. progress.md の execution_mode を agent に設定

2. progress.md の status を確認して分岐:
   ■ not_started → 全 Worker を最初から実行（ステップ3へ）
   ■ in_progress → 【再開モード】で再開位置を特定してから3へ
   ■ blocked → blocked_by を報告 → 停止
   ■ completed → 「全て完了済み」と報告して終了

3. spec.md の agents セクションから実行順序を取得

4. 各 agent について以下を繰り返す:
   a. progress.md を更新
   b. 【W11】Worker 起動前フォーマット確認
   c. 【W08】logs/agent_log.md に Worker 起動ログ
   d. Worker を起動（Taskツールを使用）
   e. Worker 終了後、完了を確認
   f. 検証実行（第1層 + 第2層）
   g. 【W08】結果ログ
   h. 結果に応じて処理

   ※ Phase 1〜3は並列✅: worker_gianni, worker_moody, worker_yarus を Taskツールで同時起動

5. 全 agent 完了 → 【完了処理】へ

=== 【完了処理】 ===
1. progress.md の status を completed に変更
2. 成果物レビュー（成功基準との照合）
3. 最終の自動検証を実行
4. 作業ログに最終サマリーを追記
5. git commit（"実装完了"）
6. 完了報告: 「実装完了。成功基準の充足状況: {PASS/FAIL のサマリー}」
