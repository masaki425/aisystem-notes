#!/usr/bin/env python3
"""
Convert ASCII-art tables in code blocks to proper Markdown tables
in Chapters 7 and 8.

Targets (7 tables):
  Ch7: type変換表, label変換表, 段階2-3比較, 段階2-4比較, 4段階概要
  Ch8: 提案書→仕様書変換, ファイル役割表
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

# Each entry: (OLD, NEW, description)
REPLACEMENTS = []

# ──────────────────────────────────────────────
# 1. Ch7 7.3: type変換表 (段階1→段階2)
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
段階1 のtype           →  段階2 のtype
──────────────────────────────────────────
molecule (QT45等)      →  entity
theory (RNA World等)   →  concept
process (自己複製等)   →  process（そのまま）
property (忠実度等)    →  property（そのまま）
method (SELEX等)       →  method（そのまま）
condition (共晶氷)     →  condition（そのまま）
analysis (適応度)      →  method に統合
context (プレバイオ)   →  消滅（ノード自体がなくなるか、conceptに）
problem (鎖阻害)       →  problem（そのまま）
```""",
"""| 段階1 のtype | 段階2 のtype |
|---|---|
| molecule (QT45等) | entity |
| theory (RNA World等) | concept |
| process (自己複製等) | process（そのまま） |
| property (忠実度等) | property（そのまま） |
| method (SELEX等) | method（そのまま） |
| condition (共晶氷) | condition（そのまま） |
| analysis (適応度) | method に統合 |
| context (プレバイオ) | 消滅（ノード自体がなくなるか、conceptに） |
| problem (鎖阻害) | problem（そのまま） |""",
"Ch7 7.3: type変換表"
))

# ──────────────────────────────────────────────
# 2. Ch7 7.3: label変換表 (段階1→段階2)
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
段階1 のlabel         →  段階2 のrelation
─────────────────────────────────────────
「が触媒」            →  causes
「を支持」            →  supports
「の性質」            →  contains
「から発見」          →  produces
「より遥かに小型」    →  compares
「を緩和」            →  inhibits
「を解析」            →  supports
「に属する」          →  contains
```""",
"""| 段階1 のlabel | 段階2 のrelation |
|---|---|
| 「が触媒」 | causes |
| 「を支持」 | supports |
| 「の性質」 | contains |
| 「から発見」 | produces |
| 「より遥かに小型」 | compares |
| 「を緩和」 | inhibits |
| 「を解析」 | supports |
| 「に属する」 | contains |""",
"Ch7 7.3: label変換表"
))

# ──────────────────────────────────────────────
# 3. Ch7 7.4: 段階2 vs 段階3 比較
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
            段階2      段階3
───────────────────────────────────
ノード数     27          27
エッジ数     30          30
type分布     同一        同一
relation分布 同一        同一
```""",
"""| | 段階2 | 段階3 |
|---|---|---|
| ノード数 | 27 | 27 |
| エッジ数 | 30 | 30 |
| type分布 | 同一 | 同一 |
| relation分布 | 同一 | 同一 |""",
"Ch7 7.4: 段階2-3比較"
))

# ──────────────────────────────────────────────
# 4. Ch7 7.5: 段階2-4 比較
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
            段階2      段階3      段階4
──────────────────────────────────────────
ノード数     27         27         28 (+1)
エッジ数     30         30         32 (+2)
孤立ノード    1          1          0
概要把握     なし       なし       あり
```""",
"""| | 段階2 | 段階3 | 段階4 |
|---|---|---|---|
| ノード数 | 27 | 27 | 28 (+1) |
| エッジ数 | 30 | 30 | 32 (+2) |
| 孤立ノード | 1 | 1 | 0 |
| 概要把握 | なし | なし | あり |""",
"Ch7 7.5: 段階2-4比較"
))

# ──────────────────────────────────────────────
# 5. Ch7 7.6: 4段階概要
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
段階1  CLAUDE.md     → 全体像の把握。概ねうまくいくが揺らぐ。
段階2  + Rules       → フォーマットの固定。精度は上がるが保証なし。
段階3  + Skills      → 手順の標準化。指示しても実行が保証されない。
段階4  + Hooks       → 決定論的制御の導入。条件の遵守が保証される。
```""",
"""| 段階 | 追加した制約 | 効果 |
|---|---|---|
| 段階1 | CLAUDE.md | 全体像の把握。概ねうまくいくが揺らぐ |
| 段階2 | + Rules | フォーマットの固定。精度は上がるが保証なし |
| 段階3 | + Skills | 手順の標準化。指示しても実行が保証されない |
| 段階4 | + Hooks | 決定論的制御の導入。条件の遵守が保証される |""",
"Ch7 7.6: 4段階概要"
))

# ──────────────────────────────────────────────
# 6. Ch8 8.3: 提案書→仕様書 変換
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
提案書（意図）                    仕様書（実行可能な設計）
─────────────────                 ─────────────────────
「概念ネットワークを構築」     →  Phase A: 前処理（テキスト抽出・チャンク分割）
                                  Phase B: 構造化（ノード・エッジ抽出、5基準スコアリング）
                                  Phase C: 統合（マージ・検証・可視化）

「5基準でエッジを評価」        →  検証基準: 全エッジにscore_*フィールドが存在すること
                                  Hookの条件: validate_phase.pyが0を返すこと

「チャンクに分割して並列処理」 →  Worker A: チャンク1-3を担当
                                  Worker B: チャンク4-6を担当
                                  Lead: Workerの結果をmerge.pyで統合
```""",
"""| 提案書（意図） | 仕様書（実行可能な設計） |
|---|---|
| 「概念ネットワークを構築」 | Phase A: 前処理（テキスト抽出・チャンク分割）、Phase B: 構造化（ノード・エッジ抽出、5基準スコアリング）、Phase C: 統合（マージ・検証・可視化） |
| 「5基準でエッジを評価」 | 検証基準: 全エッジにscore_*フィールドが存在すること。Hookの条件: validate_phase.pyが0を返すこと |
| 「チャンクに分割して並列処理」 | Worker A: チャンク1-3を担当、Worker B: チャンク4-6を担当、Lead: Workerの結果をmerge.pyで統合 |""",
"Ch8 8.3: 提案書→仕様書変換"
))

# ──────────────────────────────────────────────
# 7. Ch8 8.4: ファイル役割表
# ──────────────────────────────────────────────
REPLACEMENTS.append((
"""```
意図の記録:   提案書         ← サイクルの起点。人間が書く。
仕様の記録:   仕様書         ← 提案書から構造化。AIが生成し、人間が承認する。
進捗の記録:   進捗ファイル    ← 今どこにいるか。AIが更新する。
問題の記録:   課題管理       ← 評価で発見された問題。「どこに戻るか」の判断材料。
```""",
"""| 役割 | ファイル | 説明 |
|---|---|---|
| 意図の記録 | 提案書 | サイクルの起点。人間が書く |
| 仕様の記録 | 仕様書 | 提案書から構造化。AIが生成し、人間が承認する |
| 進捗の記録 | 進捗ファイル | 今どこにいるか。AIが更新する |
| 問題の記録 | 課題管理 | 評価で発見された問題。「どこに戻るか」の判断材料 |""",
"Ch8 8.4: ファイル役割表"
))


def main():
    with open(MD_PATH, "r") as f:
        content = f.read()

    changes = 0
    for old, new, desc in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new, 1)
            changes += 1
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc} — 置換対象が見つかりませんでした")
            # Debug: try to find partial match
            first_line = old.split('\n')[1] if '\n' in old else old[:40]
            first_line = first_line.strip()[:40]
            if first_line in content:
                idx = content.find(first_line)
                line_num = content[:idx].count('\n') + 1
                print(f"   部分マッチ（'{first_line}'）あり: 行 ~{line_num}")
                ctx = content[max(0,idx-10):idx+100]
                print(f"   周辺: {repr(ctx[:80])}")

    if changes > 0:
        with open(MD_PATH, "w") as f:
            f.write(content)
        print(f"\n✅ {changes}/{len(REPLACEMENTS)} 箇所を変換しました。")
    else:
        print("\n❌ 変更はありませんでした。")


if __name__ == "__main__":
    main()
