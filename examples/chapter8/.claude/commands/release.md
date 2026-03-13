spec.md のバージョンに基づいて GitHub Release を作成する。

「バージョン情報の取得」
docs/spec.md のバージョン履歴テーブルから status が active のバージョンを取得。

「ユーザー確認後」
1. git tag v[ver]
2. git push origin v[ver]
3. gh release create v[ver] --title "v[ver]: [name]" --notes "[変更内容]"
