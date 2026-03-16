#!/usr/bin/env python3
"""
Fix the auto-compact description in Section 1.3 to align with Anthropic's
official documentation.

Changes:
1. "切り落とされる" → 要約・圧縮であることを説明
2. "予告なく起きる" → ツールによる差異を注記
3. 「ある/ないの二値」との整合性を注記で補足
4. 小見出しを「机から書類が落ちる」→「机の書類が要約される」に変更
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

OLD_TEXT = """**auto-compact — 机から書類が落ちる**

会話が長くなってウィンドウの上限を超えると、古い部分が切り落とされる。これを auto-compact と呼ぶ。文字通り「見えなくなる」のであり、AIが「忘れた」わけではない——最初から知らない状態になる。

auto-compactは予告なく起きる。「そろそろコンテキストがいっぱいです」といった警告は出ない。あるターンまでは会話の冒頭を踏まえた応答をしていたのに、次のターンで突然「その話は初耳です」という反応になる——これが起きたら、auto-compactでコンテキストの一部が失われた可能性が高い。"""

NEW_TEXT = """**auto-compact — 机の書類が要約される**

会話が長くなってウィンドウの上限に近づくと、システムが古い部分を**要約・圧縮**して空きを作る。これを auto-compact と呼ぶ。単純に切り捨てるのではなく、重要なコードや判断を残そうとする要約処理だ。しかし要約である以上、細部は失われる。元の会話の微妙なニュアンスや、具体的な数値、一度だけ言及された前提条件——こうした情報は要約から漏れやすい。

重要なのは、モデル自身はこの要約プロセスに関与しないということだ。システムが裏側で会話履歴を圧縮し、次のターンではその圧縮後のテキストがコンテキストウィンドウに入る。モデルは「要約された履歴」を読んでいるだけであり、「元の会話を覚えている」わけではない。要約に含まれなかった情報は、モデルにとって最初から存在しなかったのと同じだ。

auto-compactの発動タイミングはツールによって異なる。Claude Code（エージェントツール）では、コンテキスト残量のインジケーターが表示され、残量が25〜30%程度になると自動的に発動する。ユーザーは `/compact` コマンドで手動実行したり、何を優先的に保持すべきか指示することもできる。一方、チャットUI（claude.ai等）ではこうした制御手段が限られており、ユーザーが気づかないうちに文脈が失われることがある。あるターンまでは会話の冒頭を踏まえた応答をしていたのに、次のターンで突然「その話は初耳です」という反応になる——これが起きたら、auto-compactで文脈の一部が要約から漏れた可能性が高い。"""

def main():
    with open(MD_PATH, "r") as f:
        content = f.read()

    if OLD_TEXT not in content:
        print("❌ 置換対象のテキストが見つかりませんでした。")
        print("   先頭20文字の検索:")
        search = OLD_TEXT[:40]
        idx = content.find(search)
        if idx >= 0:
            line_num = content[:idx].count('\n') + 1
            print(f"   '{search}' は行 {line_num} で見つかりましたが、全体が一致しません。")
            # Show surrounding context
            ctx = content[idx:idx+len(OLD_TEXT)+50]
            print(f"   実際のテキスト（先頭200文字）: {repr(ctx[:200])}")
        else:
            print(f"   '{search}' すら見つかりません。")
        return

    count = content.count(OLD_TEXT)
    if count > 1:
        print(f"⚠ 置換対象が {count} 箇所見つかりました。最初の1箇所のみ置換します。")

    content = content.replace(OLD_TEXT, NEW_TEXT, 1)

    with open(MD_PATH, "w") as f:
        f.write(content)

    print("✅ auto-compact セクション（第1章1.3節）を修正しました。")
    print()
    print("変更内容:")
    print("  1. 小見出し: 「机から書類が落ちる」→「机の書類が要約される」")
    print("  2. 「切り落とされる」→「要約・圧縮して空きを作る」に修正")
    print("  3. 要約の限界（細部が失われる）を明記")
    print("  4. モデル自身は要約に関与しないことを追加")
    print("  5. ツールによる差異（Claude Code vs チャットUI）を追加")
    print("  6. /compact コマンドによる手動制御の存在を追加")


if __name__ == "__main__":
    main()
