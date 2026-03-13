# 仕様書

## バージョン履歴

| ver | 名前 | 日付 | 状態 | 備考 |
|-----|------|------|------|------|
| 1.0 | 概念ネットワーク統合 | 2026-03-13 | active | 初期実装 |

---

## 目的・成功基準（What）

### プロジェクト概要

生命の起源に関する論文3本から概念ネットワークを個別に抽出し、統合された概念ネットワーク（YAML）を構築する。

### 目的

第7章では論文1本の概念構造化を行い、CLAUDE.md → Rules → Skills → Hooks の4段階でHarnessの効果を観察した。本プロジェクトでは入力を3本に拡張し、反復サイクルを通じてHarness設計を改善するプロセスを実践する。第8章のデモとして使用する。

### 入力

| # | ファイル | 種別 | 論文 | 備考 |
|---|---------|------|------|------|
| 1 | input/science.adt2760.pdf | 論文PDF | Gianni et al. (2026) Science — QT45リボザイムによるRNA自己複製 | 第7章でも使用 |
| 2 | input/s41559-024-02461-1.pdf | 論文PDF | Moody et al. (2024) Nature Ecology & Evolution — LUCAのゲノム再構成と年代推定 | |
| 3 | input/s00239-009-9270-1.pdf | 論文PDF | Yarus et al. (2009) Journal of Molecular Evolution — 遺伝暗号の起源と立体化学仮説 | |

- 補充の要否: 不要。3本の論文のみを入力とする。外部情報の検索・補充は行わない。

### 出力

- 個別YAML: output/gianni.yaml, output/moody.yaml, output/yarus.yaml
- 統合YAML: output/merged.yaml
- 形式: YAML（下記スキーマに準拠）
- 配置場所: output/
- 利用者: 講義ノート（第8章）の読者
- 用途: 反復サイクルによるHarness改善の実例として参照
- 閲覧環境: GitHub上のexamplesディレクトリ、または講義ノート本文

### 成功基準

- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_yaml.sh全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

### 制約・注意点

- 5基準スコアリング（エッジの重み計算は行わない）
- 可視化（HTMLグラフの生成は本プロジェクトのスコープ外）
- 論文の内容に対する学術的評価
- merge.pyでexact-matchによるノードデデュプリケーション
- 論文間をまたぐエッジはLeadが追加（Claude判断可: 明示的に関連するもののみ）

---

## 実装方針（How）

### 参照ファイル

| ファイル | パス | 用途 |
|----------|------|------|
| Gianni論文 | input/science.adt2760.pdf | Phase 1 の入力 |
| Moody論文 | input/s41559-024-02461-1.pdf | Phase 2 の入力 |
| Yarus論文 | input/s00239-009-9270-1.pdf | Phase 3 の入力 |
| 第7章参照実装 | examples/chapter7/output/science_adt2760.yaml | スキーマの参照 |

### スキーマ定義

**ノードの構造**:
```yaml
nodes:
  - id: snake_case_identifier
    label: 日本語の表示名
    type: concept | entity | process | property | method | condition | problem
    description: 1〜2文の説明
```

**エッジの構造**:
```yaml
edges:
  - source: node_id
    target: node_id
    relation: causes | requires | produces | supports | inhibits | contains | compares | derives
    description: 関係の説明
```

**metadataの構造**:
```yaml
metadata:
  title: 論文タイトル
  authors: [著者リスト]
  journal: ジャーナル名
  year: 出版年
  doi: DOI
  description: 概要
```

**type許可リスト（7種）**: concept, entity, process, property, method, condition, problem
**relation許可リスト（8種）**: causes, requires, produces, supports, inhibits, contains, compares, derives

### 品質の優先順位

1. スキーマ準拠（構造的整合性）
2. 概念の網羅性（各論文の主要概念が抽出されていること）
3. 統合の整合性（論文間の関係が適切にエッジ化されていること）

### 収束条件

- 条件1: 各論文から15ノード以上が抽出されていること
- 条件2: 各論文から15エッジ以上が抽出されていること
- 条件3: 統合YAMLに論文間をつなぐエッジが1本以上存在すること

### ノード粒度

- 方針: 各論文の主要な概念・分子・プロセス・手法をノードとする。第7章（Gianni論文）の粒度を踏襲。
- ノードにする: RNAワールド仮説、QT45リボザイム、LUCA、立体化学仮説、RNA自己複製
- ノードにしない（属性として扱う）: 著者名、出版年、DOI、具体的な数値（収率、忠実度の値）

### 期待するグラフ規模

- ノード数の目安: 個別 15〜30 × 3本 → 統合後 50〜70（重複マージ後）
- エッジ数の目安: 個別 15〜30 × 3本 → 統合後 60〜100（論文間エッジ含む）

### 重視する関係の種類

- 最重要: supports（仮説の支持関係）、derives（理論の導出関係）
- 重要: causes（因果関係）、requires（前提条件）
- あれば記録: contains, compares, produces, inhibits

### 表記ルール

- 言語: 日本語（ノードのlabel、description）
- 人名: 論文のfirst authorの姓（例: Gianni, Moody, Yarus）
- 専門用語: 英語の専門用語はそのまま使用可（例: RNA World、リボザイム）

### ドメイン知識

- LUCA: Last Universal Common Ancestor（全生物の最終共通祖先）
- RNA World: RNAが遺伝情報と触媒機能の両方を担っていたとする仮説
- リボザイム: 触媒活性を持つRNA分子

### タスク分解

#### Phase 1: Gianni論文の概念抽出・YAML生成
- Task 1.1: input/science.adt2760.pdf を読み込み、主要概念を抽出する
- Task 1.2: ノードとエッジを定義し、output/gianni.yaml を生成する
- Task 1.3: スキーマ準拠を確認する（validate_phase.py --phase 1）

#### Phase 2: Moody論文の概念抽出・YAML生成
- Task 2.1: input/s41559-024-02461-1.pdf を読み込み、主要概念を抽出する
- Task 2.2: ノードとエッジを定義し、output/moody.yaml を生成する
- Task 2.3: スキーマ準拠を確認する（validate_phase.py --phase 2）

#### Phase 3: Yarus論文の概念抽出・YAML生成
- Task 3.1: input/s00239-009-9270-1.pdf を読み込み、主要概念を抽出する
- Task 3.2: ノードとエッジを定義し、output/yarus.yaml を生成する
- Task 3.3: スキーマ準拠を確認する（validate_phase.py --phase 3）

#### Phase 4: 個別YAMLのマージ・論文間エッジ追加
- Task 4.1: 3本の個別YAMLを読み込み、merge.py でマージする
- Task 4.2: 論文間をまたぐエッジをLeadが追加する（明示的に関連するもののみ）
- Task 4.3: 統合YAMLの検証（validate_phase.py --final）

> Phase 1〜3は独立に実行可能（並列✅）。Phase 4はPhase 1〜3の完了後に実行する。

### 検証方法

#### 各 Phase 完了時（個別YAML検証 — 9項目チェック）
1. output/ にYAMLファイルが存在するか
2. nodesセクションが存在するか
3. edgesセクションが存在するか
4. ノードが1個以上あるか
5. エッジが1個以上あるか
6. エッジのsource/targetがnodesのIDに存在するか
7. 孤立ノード（どのエッジからも参照されないノード）がないか
8. typeが許可リスト7種に含まれるか
9. relationが許可リスト8種に含まれるか

#### 最終検証（統合YAML検証 — 上記9項目 + 追加1項目）
10. 3本すべての論文由来のノードが含まれていること（metadataのdoiで確認）

### 自動検証（v16）

| Phase | コマンド | 検証内容 |
|-------|---------|----------|
| 1     | `python3 scripts/validate_phase.py --phase 1` | gianni.yaml の9項目チェック |
| 2     | `python3 scripts/validate_phase.py --phase 2` | moody.yaml の9項目チェック |
| 3     | `python3 scripts/validate_phase.py --phase 3` | yarus.yaml の9項目チェック |
| final | `python3 scripts/validate_phase.py --final`   | merged.yaml の10項目チェック |

> **【W09】スキーマ変更時の注意**: spec.md の YAML スキーマ定義を変更した場合は、
> `scripts/validate_phase.py` の該当チェック項目を必ず同時に更新すること。

#### スキーマ定義と検証スクリプトの対応表（W09）

| スキーマフィールド | validate_phase.py の確認箇所 | 最終更新バージョン |
|------------------|------------------------------|------------------|
| nodes[].id | validate_individual() — ID存在確認 | 1.0 |
| nodes[].type | validate_individual() — type許可リスト確認 | 1.0 |
| edges[].source/target | validate_individual() — 参照先ノード存在確認 | 1.0 |
| edges[].relation | validate_individual() — relation許可リスト確認 | 1.0 |
| metadata.doi | validate_final() — 3本のDOI存在確認 | 1.0 |

### 自動レビュー基準（v17・第2層）

| Phase | レビュー観点 | 重大度 |
|-------|-------------|--------|
| 1-3 | 各論文の主要概念が15ノード以上抽出されているか | 中 |
| 1-3 | エッジが15本以上で主要関係が含まれているか | 中 |
| final | 論文間エッジが存在し意味的に妥当か | 中 |

#### レビュー実行設定

| 設定 | 値 | 説明 |
|------|-----|------|
| review_mode | per_phase | 全Phase完了時にレビュー |
| severity_threshold | 中 | この重大度以上で停止 |
| codex_timeout | 300 | Codex CLI のタイムアウト（秒） |

### エージェント定義（v17）

| ID | 名前 | 担当 Phase | 定義ファイル | 入力 | 出力 | 最低限チェック項目（W11） |
|----|------|-----------|-------------|------|------|--------------------------|
| worker_gianni | Gianni論文抽出 | Phase 1 | .claude/agents/worker_gianni.md | input/science.adt2760.pdf | output/gianni.yaml | `nodes:` キー存在、`edges:` キー存在、`metadata:` キー存在 |
| worker_moody | Moody論文抽出 | Phase 2 | .claude/agents/worker_moody.md | input/s41559-024-02461-1.pdf | output/moody.yaml | `nodes:` キー存在、`edges:` キー存在、`metadata:` キー存在 |
| worker_yarus | Yarus論文抽出 | Phase 3 | .claude/agents/worker_yarus.md | input/s00239-009-9270-1.pdf | output/yarus.yaml | `nodes:` キー存在、`edges:` キー存在、`metadata:` キー存在 |

#### 実行順序
worker_gianni ∥ worker_moody ∥ worker_yarus → Lead（Phase 4: merge.py + 論文間エッジ追加）

> Phase 1〜3は並列✅（Taskツールで同時起動）。Phase 4はLeadが直接実行。

#### 並列化設定

| 設定 | 値 | 説明 |
|------|-----|------|
| parallel_workers | 3 | Phase 1〜3を同時実行 |

並列化の理由: 3本の論文は入力・出力ともに独立しており、Worker間の依存関係がない。並列実行により処理時間を短縮できる。

#### エージェント間の契約

| 接続 | ファイル | フォーマット | 検証方法 |
|------|---------|-------------|----------|
| worker_gianni → Lead | output/gianni.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 1 |
| worker_moody → Lead | output/moody.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 2 |
| worker_yarus → Lead | output/yarus.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 3 |
| Lead → output | output/merged.yaml | YAML（スキーマ定義準拠） | validate_phase.py --final |

### マージ方針

- マージツール: merge.py（exact-matchによるノードデデュプリケーション）
- 手順:
  1. 3本の個別YAMLを読み込む
  2. ノードIDが完全一致するものを統合（exact-match）
  3. 全エッジを統合
  4. 論文間をまたぐエッジをLeadが追加（Claude判断可: 明示的に関連するもののみ）
  5. 統合YAMLをoutput/merged.yamlに出力

### 技術詳細

#### 使用ライブラリ
- PyYAML: YAML解析

#### ファイル構成
- scripts/validate_phase.py: 自動検証（9項目 + 統合検証）
- scripts/merge.py: 個別YAMLのマージ
- scripts/auto_review.py: 第2層自動レビュー

#### 処理フロー
1. Phase 1〜3: 各Workerが論文PDFを読み込み、概念ネットワークYAMLを生成（並列実行）
2. Phase 4: merge.pyで3本のYAMLを統合 → Leadが論文間エッジを追加
3. 最終検証: 統合YAMLの10項目チェック
