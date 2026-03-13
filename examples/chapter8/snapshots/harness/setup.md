以下の手順を実行して。

※ このコマンドは proposal.md からプロジェクトのファイル一式を生成する
※ 実行後は /execute で実装を開始できる（先に確認したい場合は /design-review）
※ テンプレートは RUN.md のテンプレートパスから読み込む（既に読み込み済みの場合はスキップ）

⚠️ **参照するテンプレートは workflow_template_v19-*.md のみ。v18 以前は参照しない。**

【前提確認】
1. proposal.md が存在するか確認（プロジェクトルート → docs/ の順で探す）
   - 存在しない → 以下を出力して停止:
     「proposal.md が見つかりません。
      proposal.md を作成してプロジェクトルートに配置してください。
      テンプレート: workflow_template_v19-proposal.md 参照」
2. proposal.md を読む

【spec.md 生成】
4. workflow_template_v19-command.md の「spec.md の対応表」を参照
5. proposal.md の各セクションから spec.md の対応項目を導出:
   - プロジェクト概要 ← A1
   - 目的           ← A2
   - 成功基準       ← A3
   - 入力           ← D1, B1
   - 出力           ← D2, A6
   - 制約           ← D6, A4
   - タスク分解     ← D3, B1-B6, C1-C6（「Claude判断可」のみ Claude が決定）
   - 検証方法       ← D5
   - エージェント定義 ← D4（並列化設定 parallel_workers も反映）
6. docs/spec.md を生成・保存
7. 「✅ docs/spec.md を生成しました」と出力

【ディレクトリ構造の作成】
8. 以下のディレクトリを作成（存在する場合はスキップ）:
   data/, data/raw/, data/references/
   output/
   logs/
   .claude/commands/, .claude/rules/
   scripts/
   .claude/agents/

【ファイル一式の生成】
9. workflow_template_v19-*.md テンプレートから生成する

【git 初期化】
10. .git が存在しない場合:
    - git init を実行
    - 「git を初期化しました」と出力

【完了報告】
11. 生成したファイルの一覧を出力
12. 以下を出力して終了:
    「✅ /setup 完了。ここで停止します。

    ⚠️ Slash Commands を使うには Claude Code を再起動してください。
    （セッション開始時に .claude/commands/ が読み込まれるため）

    次のステップ:
    1. Claude Code を再起動する
    2. docs/spec.md の内容を確認・承認する
    3. /design-review で設計確認（推奨）
    4. /execute で実装を開始する

    ※ /execute や実装には進まないでください。このコマンドはセットアップのみを行います。」
