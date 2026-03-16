#!/usr/bin/env python3
"""
Fix the 2 remaining ASCII tables that failed in convert_tables_ch7_ch8.py.
Uses regex to handle separator line length and whitespace variations.
"""
import re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "ai_system_architecture_lecture.md")

with open(MD_PATH, "r") as f:
    content = f.read()

changes = 0

# ──────────────────────────────────────────────
# 1. Ch7 7.3: type変換表
#    Left column uses half-width (), right uses full-width （）
# ──────────────────────────────────────────────
pattern1 = re.compile(
    r'```\n'
    r'段階1 のtype\s+→\s+段階2 のtype\n'
    r'─+\n'
    r'molecule \(QT45等\)\s+→\s+entity\n'
    r'theory \(RNA World等\)\s+→\s+concept\n'
    r'process \(自己複製等\)\s+→\s+process（そのまま）\n'
    r'property \(忠実度等\)\s+→\s+property（そのまま）\n'
    r'method \(SELEX等\)\s+→\s+method（そのまま）\n'
    r'condition \(共晶氷\)\s+→\s+condition（そのまま）\n'
    r'analysis \(適応度\)\s+→\s+method に統合\n'
    r'context \(プレバイオ\)\s+→\s+消滅（ノード自体がなくなるか、conceptに）\n'
    r'problem \(鎖阻害\)\s+→\s+problem（そのまま）\n'
    r'```'
)

replacement1 = """| 段階1 のtype | 段階2 のtype |
|---|---|
| molecule (QT45等) | entity |
| theory (RNA World等) | concept |
| process (自己複製等) | process（そのまま） |
| property (忠実度等) | property（そのまま） |
| method (SELEX等) | method（そのまま） |
| condition (共晶氷) | condition（そのまま） |
| analysis (適応度) | method に統合 |
| context (プレバイオ) | 消滅（ノード自体がなくなるか、conceptに） |
| problem (鎖阻害) | problem（そのまま） |"""

if pattern1.search(content):
    content = pattern1.sub(replacement1, content, count=1)
    changes += 1
    print("✅ Ch7 7.3: type変換表")
else:
    print("❌ Ch7 7.3: type変換表 — 見つかりません")
    if "| molecule (QT45等) | entity |" in content:
        print("   → 既に変換済み")

# ──────────────────────────────────────────────
# 2. Ch7 7.4: 段階2 vs 段階3
# ──────────────────────────────────────────────
pattern2 = re.compile(
    r'```\n'
    r'\s+段階2\s+段階3\n'
    r'─+\n'
    r'ノード数\s+27\s+27\n'
    r'エッジ数\s+30\s+30\n'
    r'type分布\s+同一\s+同一\n'
    r'relation分布\s+同一\s+同一\n'
    r'```'
)

replacement2 = """| | 段階2 | 段階3 |
|---|---|---|
| ノード数 | 27 | 27 |
| エッジ数 | 30 | 30 |
| type分布 | 同一 | 同一 |
| relation分布 | 同一 | 同一 |"""

if pattern2.search(content):
    content = pattern2.sub(replacement2, content, count=1)
    changes += 1
    print("✅ Ch7 7.4: 段階2-3比較")
else:
    print("❌ Ch7 7.4: 段階2-3比較 — 見つかりません")

if changes > 0:
    with open(MD_PATH, "w") as f:
        f.write(content)
    print(f"\n✅ {changes} 箇所を変換しました。合計 7/7 完了。")
else:
    print("\n❌ 変更はありませんでした。")
