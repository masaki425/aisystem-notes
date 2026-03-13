# 仕様書

## バージョン履歴

| ver | 名前 | 日付 | 状態 | 備考 |
|-----|------|------|------|------|
| 1.0 | 概念ネットワーク統合 | 2026-03-13 | archived | 初期実装（サイクル1） |
| 1.1 | 概念ネットワーク統合 | 2026-03-13 | archived | seed list追加（サイクル2） |
| 1.2 | 概念ネットワーク統合 | 2026-03-13 | active | 収束条件強化・seed list厳格化（サイクル3） |

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

### 出力

- 個別YAML: output/gianni.yaml, output/moody.yaml, output/yarus.yaml
- 統合YAML: output/merged.yaml
- 形式: YAML（下記スキーマに準拠）
- 配置場所: output/
- 用途: 講義ノート（第8章）の読者が、反復サイクルによるHarness改善の実例として参照。GitHub上のexamplesディレクトリまたは講義ノート本文から閲覧。

### 成功基準

- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_phase.py全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

### 制約・注意点

- 5基準スコアリング（エッジの重み計算）は行わない
- 可視化（HTMLグラフの生成）はスコープ外
- 論文の内容に対する学術的評価は行わない
- マージツール: merge.py（exact-matchによるノードデデュプリケーション）
- マージ手順:
  1. 3本の個別YAMLを読み込む
  2. ノードIDが完全一致するものを統合（exact-match）
  3. 全エッジを統合
  4. 論文間をまたぐエッジをLeadが追加（明示的に関連するもののみ）
  5. 統合YAMLをoutput/merged.yamlに出力

### 品質の優先順位

1. スキーマ準拠（構造的整合性）
2. 概念の網羅性（各論文の主要概念が抽出されていること）
3. 統合の整合性（論文間の関係が適切にエッジ化されていること）

---

## 実装方針（How）

### 参照ファイル

| ファイル | パス | 用途 |
|----------|------|------|
| 提案書 | docs/proposal.md | 全工程のインプット定義 |
| 環境設定 | docs/task_config.md | パス・規約 |
| 進捗管理 | docs/progress.md | 進捗管理 |
| 問題記録 | logs/issues.md | 発見した問題 |
| エージェントログ | logs/agent_log.md | エージェント実行ログ |

### タスク分解

#### Phase 1: Gianni論文の概念抽出・YAML生成（Worker A: worker_gianni）
- Task 1.1: input/science.adt2760.pdf を読み込み、概念ネットワークを抽出
- Task 1.2: output/gianni.yaml を生成（スキーマ準拠）
- Task 1.3: validate_phase.py --phase 1 で検証

#### Phase 2: Moody論文の概念抽出・YAML生成（Worker B: worker_moody）
- Task 2.1: input/s41559-024-02461-1.pdf を読み込み、概念ネットワークを抽出
- Task 2.2: output/moody.yaml を生成（スキーマ準拠）
- Task 2.3: validate_phase.py --phase 2 で検証

#### Phase 3: Yarus論文の概念抽出・YAML生成（Worker C: worker_yarus）
- Task 3.1: input/s00239-009-9270-1.pdf を読み込み、概念ネットワークを抽出
- Task 3.2: output/yarus.yaml を生成（スキーマ準拠）
- Task 3.3: validate_phase.py --phase 3 で検証

#### Phase 4: 統合YAML生成（Lead）
- Task 4.1: merge.py で3本の個別YAMLをマージ
- Task 4.2: 論文間エッジを追加（明示的に関連するもののみ）
- Task 4.3: validate_phase.py --final で最終検証

**Phase 1〜3は独立に実行可能（並列✅）。Phase 4はPhase 1〜3の完了後に実行。**

### YAMLスキーマ定義

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

### 表記ルール（B5）

- 言語: 日本語（ノードのlabel、description）
- 人名: 論文のfirst authorの姓（例: Gianni, Moody, Yarus）
- 専門用語: 英語の専門用語はそのまま使用可（例: RNA World、リボザイム）
- ノードID命名規則:
  - snake_caseで記述する
  - 英語表記で統一する（日本語をローマ字にしない）
  - 概念の最も一般的な名称を使う（例: `rna_world` ✅、`rna_world_hypothesis` ❌）

### 共通ノード seed list（全Workerが使用すること）

以下のノードは3本の論文にまたがって登場する可能性がある概念である。
該当する概念が論文中に登場した場合、以下のIDとtypeを使用すること。
論文固有の詳細はdescriptionに記述する。

| id | label | type | 該当する論文 |
|----|-------|------|-------------|
| `rna_world` | RNAワールド | concept | Gianni, Moody, Yarus |
| `luca` | LUCA（全生物最終共通祖先） | concept | Moody（Gianni, Yarusでも言及があれば使用） |
| `genetic_code` | 遺伝暗号 | concept | Yarus, Moody |
| `in_vitro_selection` | in vitro選択 | method | Gianni, Yarus |
| `prebiotic_chemistry` | プレバイオティック化学 | concept | Gianni, Moody（Yarusでも言及があれば使用） |
| `rna_self_replication` | RNA自己複製 | process | Gianni（Yarusでも言及があれば使用） |

**seed list運用ルール（v1.2）**:
- 「該当する論文」に名前が挙がっている場合、**その論文でノードが登場しないことはありえない**。Workerは必ずそのIDでノードを作成し、論文における文脈をdescriptionに記述すること。
- Moody論文は `rna_world` と `genetic_code` を必ず使用すること（v1.2で明示的に要求）。

### 収束条件（B3）

- 条件1: 各論文から15ノード以上が抽出されていること
- 条件2: 各論文から15エッジ以上が抽出されていること
- 条件3: 統合YAMLにおいて、各論文ペア間（G-M, G-Y, M-Y）にそれぞれ2本以上の論文間エッジが存在すること
- 条件4: 統合後に他論文と接続のないノードが全体の60%以下であること

### ノード粒度（C1）

- 方針: 各論文の主要な概念・分子・プロセス・手法をノードとする。第7章（Gianni論文）の粒度を踏襲。
- ノードにする: RNAワールド仮説、QT45リボザイム、LUCA、立体化学仮説、RNA自己複製
- ノードにしない（属性として扱う）: 著者名、出版年、DOI、具体的な数値

### 期待するグラフ規模（C2）

- ノード数の目安: 個別 15〜30 × 3本 → 統合後 50〜70（重複マージ後）
- エッジ数の目安: 個別 15〜30 × 3本 → 統合後 60〜100（論文間エッジ含む）

### 重視する関係の種類（C3）

- 最重要: supports（仮説の支持関係）、derives（理論の導出関係）
- 重要: causes（因果関係）、requires（前提条件）
- あれば記録: contains, compares, produces, inhibits

### エッジの閾値方針（C4）

- 方針: 全ペア（明示的に関連するもののみ）
- 潜在的関係: 記録しない

### ドメイン知識（B6）

- LUCA: Last Universal Common Ancestor（全生物の最終共通祖先）
- RNA World: RNAが遺伝情報と触媒機能の両方を担っていたとする仮説
- リボザイム: 触媒活性を持つRNA分子

### 検証方法

#### 各Phase完了時（Phase 1〜3: 個別YAML検証）

validate_phase.py による9項目チェック:
1. output/ にYAMLファイルが存在するか
2. nodesセクションが存在するか
3. edgesセクションが存在するか
4. ノードが1個以上あるか
5. エッジが1個以上あるか
6. エッジのsource/targetがnodesのIDに存在するか
7. 孤立ノード（どのエッジからも参照されないノード）がないか
8. typeが許可リスト7種に含まれるか
9. relationが許可リスト8種に含まれるか

#### Phase 4完了時（統合YAML検証）

上記9項目に加えて:
10. 3本すべての論文由来のノードが含まれていること（metadataのdoiで確認）

#### 最終検証

- 成功基準（A3）の4項目すべてを確認
- 収束条件（B3）の4項目すべてを確認

### 自動検証（v16）

| Phase | コマンド | 検証内容 |
|-------|---------|----------|
| 1 | `python3 scripts/validate_phase.py --phase 1` | gianni.yaml の9項目チェック |
| 2 | `python3 scripts/validate_phase.py --phase 2` | moody.yaml の9項目チェック |
| 3 | `python3 scripts/validate_phase.py --phase 3` | yarus.yaml の9項目チェック |
| final | `python3 scripts/validate_phase.py --final` | 統合YAML + 成功基準 + 収束条件の照合 |

> ⚠️ **【W09】スキーマ変更時の注意**: spec.md の YAML スキーマ定義を変更した場合は、
> `scripts/validate_phase.py` の該当チェック項目を必ず同時に更新すること。

#### スキーマ定義と検証スクリプトの対応表（W09）

| スキーマフィールド | validate_phase.py の確認箇所 | 最終更新バージョン |
|------------------|------------------------------|------------------|
| nodes[].id | validate_individual() - ノードID存在チェック | 1.0 |
| nodes[].type | validate_individual() - type許可リスト7種チェック | 1.0 |
| edges[].relation | validate_individual() - relation許可リスト8種チェック | 1.0 |
| edges[].source/target | validate_individual() - ノードID参照チェック | 1.0 |
| metadata.doi | validate_final() - 3論文DOI存在チェック | 1.0 |

### 自動レビュー基準（v17・第2層）

| Phase | レビュー観点 | 重大度 |
|-------|-------------|--------|
| 1-3 | 各論文の主要概念が15ノード以上抽出されているか | 中 |
| 1-3 | seed listのIDが正しく使用されているか | 中 |
| 4 | 論文間エッジが各ペア2本以上存在するか | 中 |
| 4 | 他論文と未接続のノードが60%以下か | 中 |

#### レビュー実行設定

| 設定 | 値 | 説明 |
|------|-----|------|
| review_mode | per_phase | 全Phase完了時にレビュー |
| severity_threshold | 中 | この重大度以上で停止 |
| codex_timeout | 300 | Codex CLI のタイムアウト（秒） |

### エージェント定義（v19）

| ID | 名前 | 担当 Phase | 定義ファイル | 入力 | 出力 | 最低限チェック項目（W11） |
|----|------|-----------|-------------|------|------|--------------------------|
| worker_gianni | Gianni論文抽出 | Phase 1 並列✅ | .claude/agents/worker_gianni.md | input/science.adt2760.pdf | output/gianni.yaml | `nodes:` キー存在、`edges:` キー存在 |
| worker_moody | Moody論文抽出 | Phase 2 並列✅ | .claude/agents/worker_moody.md | input/s41559-024-02461-1.pdf | output/moody.yaml | `nodes:` キー存在、`edges:` キー存在 |
| worker_yarus | Yarus論文抽出 | Phase 3 並列✅ | .claude/agents/worker_yarus.md | input/s00239-009-9270-1.pdf | output/yarus.yaml | `nodes:` キー存在、`edges:` キー存在 |

#### 実行順序

worker_gianni, worker_moody, worker_yarus（並列✅同時起動） → Lead（Phase 4: merge.py + 論文間エッジ追加）

#### エージェント間の契約

| 接続 | ファイル | フォーマット | 検証方法 |
|------|---------|-------------|----------|
| worker_gianni → Lead | output/gianni.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 1 |
| worker_moody → Lead | output/moody.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 2 |
| worker_yarus → Lead | output/yarus.yaml | YAML（スキーマ定義準拠） | validate_phase.py --phase 3 |

#### 並列化設定

| 設定 | 値 | 説明 |
|------|-----|------|
| parallel_workers | 3 | Phase 1〜3を同時実行 |
| 並列化の理由 | 3本の論文は入力・出力ともに独立しており、Worker間の依存関係がない | |

### 技術詳細

#### 使用ライブラリ
- PyYAML: YAML解析（検証スクリプト、マージスクリプト）

#### ファイル構成
- scripts/validate_phase.py: 自動検証スクリプト（9項目 + 統合検証）
- scripts/merge.py: 個別YAML統合スクリプト（exact-match）
- scripts/auto_review.py: 自動レビュースクリプト（第2層）

#### 処理フロー
1. Phase 1〜3: 各WorkerがPDFを読み、概念ネットワークをYAML化（並列実行）
2. Phase 4: merge.pyで3本のYAMLを統合 → Leadが論文間エッジを追加
3. 最終検証: 成功基準・収束条件の全項目を確認
