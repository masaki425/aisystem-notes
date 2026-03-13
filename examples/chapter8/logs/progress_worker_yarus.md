# Worker Progress: worker_yarus

## 担当
- Phase: 3
- 入力: input/s00239-009-9270-1.pdf
- 出力: output/yarus.yaml

## 状態
- status: completed
- spec_version: 1.1

## 実行結果
- ノード数: 22
- エッジ数: 21
- seed list使用: genetic_code, in_vitro_selection, rna_world（3/6該当）
- 検証（第1層）: PASS
- 命名規則: snake_case、英語表記、seed list準拠

## 完了条件チェック
- [x] nodes: キー存在
- [x] edges: キー存在
- [x] metadata: キー存在
- [x] 15ノード以上: 22ノード
- [x] 15エッジ以上: 21エッジ
- [x] 孤立ノードなし
- [x] type許可リスト準拠
- [x] relation許可リスト準拠
- [x] seed listに該当する概念が指定IDで登録されている
