ローカルの変更を GitHub にアップロードする。

「前提確認」
1. git が初期化されているか確認（git status）
2. GitHub CLI（gh）がインストールされているか確認（which gh）
3. GitHub にログイン済みか確認（gh auth status）

「リモートリポジトリ確認」
git remote -v でリモートが設定済みか確認する。

■ 未設定の場合（初回）
1. CLAUDE.md のプロジェクト名からリポジトリ名を決定
2. ユーザーに確認後: gh repo create [名前] --private --source=. --push

■ 設定済みの場合 → そのまま push へ

「アップロード実行」
1. 未コミットの変更 → git add . && git commit -m "publish: 最新の変更を反映"
2. リモートに新しい変更がある場合 → 「先に /sync を実行してください」と報告して終了
3. git push origin main
