#!/usr/bin/env python3
"""Phase 完了時の自動検証スクリプト（第1層）

概念ネットワーク統合プロジェクト用にカスタマイズ。
9項目チェック（個別YAML）+ 統合検証（merged.yaml）。

使い方:
  python3 scripts/validate_phase.py --phase 1                # gianni.yaml の検証
  python3 scripts/validate_phase.py --phase 2                # moody.yaml の検証
  python3 scripts/validate_phase.py --phase 3                # yarus.yaml の検証
  python3 scripts/validate_phase.py --phase 1 --with-review  # 第1層 + 第2層
  python3 scripts/validate_phase.py --final                  # merged.yaml の10項目チェック

終了コード:
  0 = 全チェック通過
  1 = 問題あり（issues.md に記録済み）
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# Phase番号 → YAMLファイルの対応
PHASE_FILES = {
    1: "output/gianni.yaml",
    2: "output/moody.yaml",
    3: "output/yarus.yaml",
}

# type許可リスト（7種）
ALLOWED_TYPES = {"concept", "entity", "process", "property", "method", "condition", "problem"}

# relation許可リスト（8種）
ALLOWED_RELATIONS = {"causes", "requires", "produces", "supports", "inhibits", "contains", "compares", "derives"}

# 3本の論文のDOI（統合検証用）
EXPECTED_DOIS = [
    "10.1126/science.adt2760",      # Gianni
    "10.1038/s41559-024-02461-1",   # Moody
    "10.1007/s00239-009-9270-1",    # Yarus
]


# ============================================================
# issues.md への自動記録
# ============================================================

def get_next_issue_id(issues_path: Path, prefix: str = "AUTO") -> str:
    """次の PREFIX-XXX ID を生成"""
    if not issues_path.exists():
        return f"{prefix}-001"
    content = issues_path.read_text(encoding="utf-8")
    import re
    ids = re.findall(rf"{prefix}-(\d+)", content)
    if not ids:
        return f"{prefix}-001"
    max_id = max(int(i) for i in ids)
    return f"{prefix}-{max_id + 1:03d}"


def append_issue(issues_path: Path, issue_id: str, priority: str, summary: str, detail: str, source: str = "自動検証（validate_phase.py）"):
    """issues.md に問題を追記"""
    if not issues_path.exists():
        print(f"  ⚠️ {issues_path} が存在しません。スキップします。")
        return
    content = issues_path.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    no_issue_line = "| - | - | なし | - | - |"
    summary_line = f"| {issue_id} | {priority} | {summary} | {source.split('（')[0]} | {today} |"
    if no_issue_line in content:
        content = content.replace(no_issue_line, summary_line)
    else:
        marker = "※ 問題解決時"
        if marker in content:
            content = content.replace(marker, f"{summary_line}\n\n{marker}")
    detail_entry = f"""
### {today} ID: {issue_id}
**優先度**: {priority}
**種別**: 自動検証
**検出元**: {source}
**内容**: {summary}
**影響範囲**: {detail}
**対応状況**: 未対応
"""
    content += detail_entry
    issues_path.write_text(content, encoding="utf-8")
    print(f"  📝 {issue_id} を issues.md に記録しました")


# ============================================================
# 検証関数
# ============================================================

def validate_individual(yaml_path: Path) -> list:
    """個別YAMLの9項目チェック"""
    errors = []
    import yaml

    # 1. ファイル存在
    if not yaml_path.exists():
        errors.append({"priority": "高", "summary": f"{yaml_path.name} が存在しない", "detail": f"{yaml_path} が見つからない"})
        return errors

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append({"priority": "高", "summary": f"YAML パースエラー: {e}", "detail": str(e)})
        return errors

    if data is None:
        errors.append({"priority": "高", "summary": f"{yaml_path.name} が空", "detail": "YAMLファイルの内容が空"})
        return errors

    # 2. nodesセクション存在
    if "nodes" not in data:
        errors.append({"priority": "高", "summary": f"{yaml_path.name}: nodes セクションなし", "detail": "nodesキーが存在しない"})

    # 3. edgesセクション存在
    if "edges" not in data:
        errors.append({"priority": "高", "summary": f"{yaml_path.name}: edges セクションなし", "detail": "edgesキーが存在しない"})

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # 4. ノードが1個以上
    if len(nodes) < 1:
        errors.append({"priority": "高", "summary": f"{yaml_path.name}: ノードが0個", "detail": "ノードが1個以上必要"})

    # 5. エッジが1個以上
    if len(edges) < 1:
        errors.append({"priority": "高", "summary": f"{yaml_path.name}: エッジが0個", "detail": "エッジが1個以上必要"})

    # 6. エッジのsource/targetがnodesのIDに存在するか
    node_ids = {n.get("id") for n in nodes}
    for edge in edges:
        src = edge.get("source", "")
        tgt = edge.get("target", "")
        if src not in node_ids:
            errors.append({"priority": "高", "summary": f"{yaml_path.name}: エッジのsource '{src}' がnodesに存在しない", "detail": f"edge: {src} -> {tgt}"})
        if tgt not in node_ids:
            errors.append({"priority": "高", "summary": f"{yaml_path.name}: エッジのtarget '{tgt}' がnodesに存在しない", "detail": f"edge: {src} -> {tgt}"})

    # 7. 孤立ノード
    referenced_ids = set()
    for edge in edges:
        referenced_ids.add(edge.get("source", ""))
        referenced_ids.add(edge.get("target", ""))
    orphans = node_ids - referenced_ids
    if orphans:
        errors.append({"priority": "中", "summary": f"{yaml_path.name}: 孤立ノード {len(orphans)}個", "detail": f"孤立ノード: {', '.join(sorted(orphans))}"})

    # 8. typeが許可リストに含まれるか
    for node in nodes:
        ntype = node.get("type", "")
        if ntype not in ALLOWED_TYPES:
            errors.append({"priority": "高", "summary": f"{yaml_path.name}: 不正なtype '{ntype}'（ノード: {node.get('id', '?')}）", "detail": f"許可リスト: {ALLOWED_TYPES}"})

    # 9. relationが許可リストに含まれるか
    for edge in edges:
        rel = edge.get("relation", "")
        if rel not in ALLOWED_RELATIONS:
            errors.append({"priority": "高", "summary": f"{yaml_path.name}: 不正なrelation '{rel}'", "detail": f"許可リスト: {ALLOWED_RELATIONS}"})

    return errors


def validate_phase(phase_num: int) -> list:
    """Phase 固有の検証"""
    yaml_file = PHASE_FILES.get(phase_num)
    if not yaml_file:
        return [{"priority": "高", "summary": f"Phase {phase_num} に対応するYAMLファイルが定義されていない", "detail": ""}]
    return validate_individual(Path(yaml_file))


def validate_final() -> list:
    """最終検証（merged.yaml の10項目チェック）"""
    errors = []
    merged_path = Path("output/merged.yaml")

    # まず9項目チェック
    errors.extend(validate_individual(merged_path))

    if not merged_path.exists():
        return errors

    import yaml
    data = yaml.safe_load(merged_path.read_text(encoding="utf-8"))
    if data is None:
        return errors

    # 10. 3本すべての論文由来のノードが含まれていること（metadataのdoiで確認）
    # merged.yaml のmetadataにsourcesリストがあると想定
    metadata = data.get("metadata", {})
    sources = metadata.get("sources", [])
    if isinstance(sources, list):
        source_dois = set()
        for src in sources:
            if isinstance(src, dict):
                doi = src.get("doi", "")
                if doi:
                    source_dois.add(doi)
        for expected_doi in EXPECTED_DOIS:
            if expected_doi not in source_dois:
                errors.append({
                    "priority": "高",
                    "summary": f"merged.yaml: DOI {expected_doi} のソースが含まれていない",
                    "detail": "3本すべての論文由来のノードが含まれている必要がある"
                })
    else:
        # sourcesが無い場合、個別のdoiフィールドを探す
        doi = metadata.get("doi", "")
        if not doi and not sources:
            errors.append({
                "priority": "中",
                "summary": "merged.yaml: metadata.sources が存在しない",
                "detail": "統合YAMLのmetadataに各論文のDOI情報が必要"
            })

    return errors


# ============================================================
# メイン処理
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Phase 完了時の自動検証")
    parser.add_argument("--phase", type=int, help="検証する Phase 番号（1=gianni, 2=moody, 3=yarus）")
    parser.add_argument("--final", action="store_true", help="最終検証（merged.yaml の10項目チェック）")
    parser.add_argument("--with-review", action="store_true", help="第2層（auto_review.py）も実行")
    parser.add_argument("--review-only", action="store_true", help="第2層のみ実行")
    parser.add_argument("--reviewer", default="codex",
                        help="第2層のレビュアーを指定（カンマ区切りで複数可: codex,gemini）")
    args = parser.parse_args()

    if not any([args.phase, args.final]):
        parser.print_help()
        sys.exit(1)

    issues_path = Path("logs/issues.md")

    # --- Phase / final 検証 ---
    if not args.review_only:
        if args.final:
            print("🔍 最終検証を実行中...（第1層）")
            errors = validate_final()
            phase_label = "最終検証"
        else:
            print(f"🔍 Phase {args.phase} の検証を実行中...（第1層）")
            errors = validate_phase(args.phase)
            phase_label = f"Phase {args.phase}"

        if errors:
            print(f"\n❌ {phase_label}: {len(errors)} 件の問題を検出（第1層）")
            for error in errors:
                issue_id = get_next_issue_id(issues_path, prefix="AUTO")
                append_issue(issues_path, issue_id, error["priority"], error["summary"], error["detail"])
            sys.exit(1)
        else:
            print(f"\n✅ {phase_label}: 第1層チェック通過")

    if args.with_review or args.review_only:
        reviewers = [r.strip() for r in (getattr(args, 'reviewer', None) or 'codex').split(',')]
        review_had_failure = False
        for reviewer in reviewers:
            print(f"\n🔍 第2層（自動レビュー）を実行中...（レビュアー: {reviewer}）")
            review_args = ["python3", "scripts/auto_review.py", "--reviewer", reviewer]
            if args.phase:
                review_args += ["--phase", str(args.phase)]
            if args.final:
                review_args += ["--final"]
            try:
                result = subprocess.run(review_args, capture_output=False, timeout=600)
                review_exit = result.returncode
            except FileNotFoundError:
                print("⚠️ auto_review.py が見つかりません。第2層をスキップして続行")
                review_exit = 2
            except subprocess.TimeoutExpired:
                print(f"⚠️ {reviewer} レビューがタイムアウトしました。スキップして続行")
                review_exit = 2

            if review_exit == 2:
                print(f"⚠️ 第2層をスキップしました（{reviewer} 利用不可）")
            elif review_exit == 1:
                print(f"\n❌ {reviewer} 第2層で問題が検出されました。issues.md を確認してください。")
                review_had_failure = True
            else:
                print(f"✅ {reviewer} 第2層チェック通過")

        if review_had_failure:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
