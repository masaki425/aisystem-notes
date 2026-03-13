#!/usr/bin/env python3
"""個別YAMLのマージスクリプト

3本の個別YAML（gianni.yaml, moody.yaml, yarus.yaml）を読み込み、
統合YAML（merged.yaml）を生成する。

マージ方針:
- ノードIDが完全一致するものを統合（exact-match）
- 全エッジを統合
- 重複エッジ（同一source-target-relation）は除去

使い方:
  python3 scripts/merge.py
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ PyYAML が必要です: pip install pyyaml")
    sys.exit(1)


INPUT_FILES = [
    ("output/gianni.yaml", "Gianni et al. (2026)"),
    ("output/moody.yaml", "Moody et al. (2024)"),
    ("output/yarus.yaml", "Yarus et al. (2009)"),
]

OUTPUT_FILE = "output/merged.yaml"


def load_yaml(path: str) -> dict:
    """YAMLファイルを読み込む"""
    p = Path(path)
    if not p.exists():
        print(f"❌ {path} が見つかりません")
        sys.exit(1)
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def merge_yamls(inputs: list) -> dict:
    """複数のYAMLを統合する"""
    all_nodes = {}
    all_edges = []
    sources_metadata = []

    for filepath, label in inputs:
        data = load_yaml(filepath)

        # ノードの統合（exact-match by id）
        for node in data.get("nodes", []):
            node_id = node.get("id", "")
            if node_id not in all_nodes:
                all_nodes[node_id] = node
            # 完全一致IDの場合はスキップ（最初のもの優先）

        # エッジの統合
        for edge in data.get("edges", []):
            all_edges.append(edge)

        # メタデータ収集
        metadata = data.get("metadata", {})
        if metadata:
            sources_metadata.append(metadata)

    # 重複エッジの除去（source + target + relation が同一のもの）
    seen_edges = set()
    unique_edges = []
    for edge in all_edges:
        key = (edge.get("source", ""), edge.get("target", ""), edge.get("relation", ""))
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(edge)

    merged = {
        "metadata": {
            "title": "概念ネットワーク統合 — 生命の起源に関する3論文",
            "description": "Gianni, Moody, Yarus の3論文から抽出した概念ネットワークの統合",
            "sources": sources_metadata,
        },
        "nodes": list(all_nodes.values()),
        "edges": unique_edges,
    }

    return merged


def main():
    print("🔄 個別YAMLのマージを開始...")

    # 入力ファイルの存在確認
    for filepath, label in INPUT_FILES:
        if not Path(filepath).exists():
            print(f"❌ {filepath} が見つかりません。Phase 1〜3が完了しているか確認してください。")
            sys.exit(1)
        print(f"  📄 {filepath} ({label})")

    # マージ実行
    merged = merge_yamls(INPUT_FILES)

    # 統計
    node_count = len(merged["nodes"])
    edge_count = len(merged["edges"])
    source_count = len(merged["metadata"]["sources"])

    # 出力
    output_path = Path(OUTPUT_FILE)
    output_path.write_text(
        yaml.dump(merged, allow_unicode=True, default_flow_style=False, sort_keys=False),
        encoding="utf-8"
    )

    print(f"\n✅ マージ完了: {OUTPUT_FILE}")
    print(f"  ノード数: {node_count}")
    print(f"  エッジ数: {edge_count}")
    print(f"  ソース数: {source_count}")


if __name__ == "__main__":
    main()
