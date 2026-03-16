#!/usr/bin/env python3
"""Phase 完了時の自動レビュースクリプト（第2層）

外部 AI モデルを CLI 経由で呼び出し、成果物をレビューする。
validate_phase.py --with-review から呼び出される。

使い方:
  python3 scripts/auto_review.py --phase 1                      # デフォルトレビュアーでレビュー
  python3 scripts/auto_review.py --phase 1 --reviewer codex     # Codex でレビュー
  python3 scripts/auto_review.py --phase 1 --reviewer gemini    # Gemini でレビュー
  python3 scripts/auto_review.py --final --reviewer codex       # 最終検証 + Codex

終了コード:
  0 = 問題なし
  1 = 問題あり（issues.md に記録済み）
  2 = レビュアーが利用不可（スキップ）
"""

import argparse
import subprocess
import sys
from pathlib import Path


# ============================================================
# レビュアー定義
# ============================================================

REVIEWERS = {
    "codex": {
        "cmd": ["codex", "exec", "--sandbox", "read-only", "--cd", "."],
        "prompt_flag": None,
        "prefix": "CODEX",
    },
    "gemini": {
        "cmd": ["gemini", "-p"],
        "prompt_flag": None,
        "prefix": "GEMINI",
    },
    "claude": {
        "cmd": ["claude", "--print"],
        "prompt_flag": None,
        "prefix": "CLAUDE",
    },
}

DEFAULT_REVIEWER = "codex"


# ============================================================
# レビュープロンプト構築
# ============================================================

def build_review_prompt(phase_num: int = None, is_final: bool = False) -> str:
    """外部レビュアーに渡すプロンプトを組み立てる"""
    prompt = """このプロジェクトの実装結果をレビューしてください。

## レビュー対象
1. docs/spec.md の成功基準を確認
2. output/ の成果物が成功基準を満たしているか
3. scripts/ の検証コードの品質

## 確認観点
1. 仕様との整合性（spec.md の成功基準との照合）
2. データ品質（空フィールド、異常値、重複、フィールド名の整合性）
3. スキーマ準拠（type/relation許可リスト、ノード・エッジの必須フィールド）

## 出力形式
- 問題の重大度（Critical/Major/Minor/Info）
- 問題の内容
- 影響範囲
- 推奨する修正方法
"""
    if phase_num:
        prompt += f"\n※ 今回のレビュー対象は Phase {phase_num} の成果物です。\n"
    if is_final:
        prompt += "\n※ これは最終検証です。全体を通してレビューしてください。\n"
    return prompt


# ============================================================
# レビュー実行
# ============================================================

def run_review(reviewer_name: str, prompt: str, timeout: int = 600) -> tuple:
    """外部レビュアーを実行して結果を返す"""
    reviewer = REVIEWERS.get(reviewer_name)
    if not reviewer:
        print(f"⚠️ 不明なレビュアー: {reviewer_name}（利用可能: {', '.join(REVIEWERS.keys())}）")
        return 2, ""

    cmd = reviewer["cmd"] + [prompt]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout
    except FileNotFoundError:
        print(f"⚠️ {reviewer_name} CLI が見つかりません。インストールしてください。")
        return 2, ""
    except subprocess.TimeoutExpired:
        print(f"⚠️ {reviewer_name} レビューがタイムアウトしました（{timeout}秒）")
        return 2, ""


# ============================================================
# メイン
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="第2層自動レビュー（外部AI）")
    parser.add_argument("--phase", type=int, help="レビュー対象の Phase 番号")
    parser.add_argument("--final", action="store_true", help="最終検証モード")
    parser.add_argument("--reviewer", default=DEFAULT_REVIEWER,
                        choices=list(REVIEWERS.keys()),
                        help=f"レビュアーを指定（デフォルト: {DEFAULT_REVIEWER}）")
    parser.add_argument("--timeout", type=int, default=600,
                        help="タイムアウト秒数（デフォルト: 600）")
    args = parser.parse_args()

    prompt = build_review_prompt(args.phase, args.final)

    phase_label = f"Phase {args.phase}" if args.phase else "最終検証"
    print(f"🔍 第2層レビュー: {phase_label}（レビュアー: {args.reviewer}）")

    exit_code, output = run_review(args.reviewer, prompt, args.timeout)

    if exit_code == 2:
        print(f"⚠️ 第2層をスキップしました（{args.reviewer} 利用不可）")
        sys.exit(2)

    if output:
        print(f"\n--- {args.reviewer} レビュー結果 ---")
        print(output)
        print("--- レビュー結果終わり ---")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
