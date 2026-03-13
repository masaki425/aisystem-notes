# Harness — 基盤構造

本ディレクトリには、第8章デモの基盤構造を構成するキーファイルのコピーを置いている。実際にClaude Codeが読むファイルは `.claude/commands/` および `.claude/settings.json` にあるが、ドットディレクトリは見落としやすいため、ここに参照用コピーを配置した。

## ファイル一覧

### setup.md — セットアップコマンド（/setup）

proposal.mdを読み、プロジェクトに必要なファイル一式を自動生成するSlash Command。

主な処理:
1. proposal.mdの存在確認
2. proposal.mdの各セクション（A〜F）からspec.mdを導出
3. ディレクトリ構造の作成
4. Worker定義、検証スクリプト、進捗管理ファイル等を生成
5. git初期化

提案書の1箇所を変更して/setupを再実行すれば、下流のファイルが一貫して更新される。サイクル1→2ではseed listの追加がWorker定義3体に波及し、サイクル2→3では運用ルールの厳格化がWorker定義の既存項目の強度を変えた。

### execute.md — 実行コマンド（/execute）

spec.mdのタスクを実行するSlash Command。

主な処理:
1. progress.md、spec.md、CLAUDE.mdの読み込み
2. エージェントモードの判定（spec.mdにエージェント定義があるか）
3. Lead-Worker構造でPhase 1〜4を実行（Phase 1〜3は並列）
4. 各Phase完了時にvalidate_phase.pyで検証
5. 完了処理（成功基準照合、git commit）

/execute実行中はStop Hook（settings.json）がprogress.md更新とgit commitを監視する。サイクル3ではworker_moody未完了のままPhase 4に進もうとしたLeadを差し戻した。

### settings.json — Stop Hook定義

Claude Codeの実行を監視するHook設定。

Stop Hookの検査内容:
1. ファイルが変更されたか（読み取り専用操作は対象外）
2. 変更があった場合、docs/progress.mdが更新されたか
3. git commitが実行されたか

このHookが決定論的制御の核心。progress.md未更新やgit commit忘れを確実に検出して差し戻す。サイクル3・4で複数回発動し、Worker未完了やcommit漏れを防いだ。
