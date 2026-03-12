#!/bin/bash
# validate_yaml.sh - 構造化YAMLの整合性を検証する
# Hooks（Stop hook）から呼び出される決定論的チェック

OUTPUT_DIR="output"
errors=""

# 1. output/ にYAMLファイルが存在するか
yaml_files=$(find "$OUTPUT_DIR" -name "*.yaml" 2>/dev/null)
if [ -z "$yaml_files" ]; then
  errors="${errors}output/ にYAMLファイルが存在しません。\n"
fi

for yaml_file in $yaml_files; do
  # 2. nodesセクションが存在するか
  if ! grep -q "^nodes:" "$yaml_file"; then
    errors="${errors}${yaml_file}: nodesセクションが存在しません。\n"
  fi

  # 3. edgesセクションが存在するか
  if ! grep -q "^edges:" "$yaml_file"; then
    errors="${errors}${yaml_file}: edgesセクションが存在しません。\n"
  fi

  # 4. ノードが1個以上あるか
  node_count=$(grep -c "^  - id:" "$yaml_file")
  if [ "$node_count" -eq 0 ]; then
    errors="${errors}${yaml_file}: ノードが0個です。\n"
  fi

  # 5. エッジが1個以上あるか
  edge_count=$(grep -c "    relation:" "$yaml_file")
  if [ "$edge_count" -eq 0 ]; then
    errors="${errors}${yaml_file}: エッジが0個です。\n"
  fi

  # 6. エッジのsource/targetがnodesのIDに存在するか
  node_ids=$(grep "^  - id:" "$yaml_file" | sed 's/^  - id: //')
  sources=$(grep "    source:" "$yaml_file" | sed 's/.*source: //')
  targets=$(grep "    target:" "$yaml_file" | sed 's/.*target: //')

  for src in $sources; do
    if ! echo "$node_ids" | grep -q "^${src}$"; then
      errors="${errors}${yaml_file}: エッジのsource '${src}' がnodesに存在しません。\n"
    fi
  done

  for tgt in $targets; do
    if ! echo "$node_ids" | grep -q "^${tgt}$"; then
      errors="${errors}${yaml_file}: エッジのtarget '${tgt}' がnodesに存在しません。\n"
    fi
  done

  # 7. 孤立ノード（どのエッジからも参照されないノード）の検出
  all_refs=$(echo -e "${sources}\n${targets}" | sort -u)
  for nid in $node_ids; do
    if ! echo "$all_refs" | grep -q "^${nid}$"; then
      errors="${errors}${yaml_file}: ノード '${nid}' はどのエッジからも参照されていません（孤立ノード）。\n"
    fi
  done

  # 8. typeが許可リストに含まれるか
  types=$(grep "    type:" "$yaml_file" | sed 's/.*type: //')
  allowed_types="concept entity process property method condition problem"
  for t in $types; do
    if ! echo "$allowed_types" | grep -qw "$t"; then
      errors="${errors}${yaml_file}: 許可されていないtype '${t}' が使用されています。\n"
    fi
  done

  # 9. relationが許可リストに含まれるか
  relations=$(grep "    relation:" "$yaml_file" | sed 's/.*relation: //')
  allowed_relations="causes requires produces supports inhibits contains compares derives"
  for r in $relations; do
    if ! echo "$allowed_relations" | grep -qw "$r"; then
      errors="${errors}${yaml_file}: 許可されていないrelation '${r}' が使用されています。\n"
    fi
  done
done

# 結果の出力
if [ -n "$errors" ]; then
  echo "BLOCKED"
  echo "以下の問題を修正してください:"
  echo ""
  echo -e "$errors"
  exit 1
else
  echo "検証OK: YAMLの整合性チェックに合格しました。"
  echo "  ノード数: ${node_count}"
  echo "  エッジ数: ${edge_count}"
  exit 0
fi
