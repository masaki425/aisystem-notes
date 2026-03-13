GitHub から最新の変更をローカルに取り込む。

「前提確認」
1. git が初期化されているか確認
2. リモートリポジトリが設定されているか確認

「同期実行」
1. 未コミットの変更があればコミットまたは stash
2. git fetch origin
3. git pull origin main
4. stash した変更があれば git stash pop
