# 提案書（Proposal） — 概念ネットワーク統合プロジェクト

**バージョン**: v1.1
**作成日**: 2026-03-XX
**変更履歴**:

| ver | 日付 | 変更内容 |
|-----|------|---------|
| 1.0 | 2026-03-XX | 初版作成 |
| 1.1 | 2026-03-XX | B5にノードID命名規則と共通ノードseed listを追加（サイクル1で命名の揺れによるマージ品質低下を確認したため） |

---

## A. プロジェクトの定義

### A1. プロジェクト概要

生命の起源に関する論文3本から概念ネットワークを個別に抽出し、統合された概念ネットワーク（YAML）を構築する。

### A2. 目的・動機

第7章では論文1本の概念構造化を行い、CLAUDE.md → Rules → Skills → Hooks の4段階でHarnessの効果を観察した。本プロジェクトでは入力を3本に拡張し、反復サイクルを通じてHarness設計を改善するプロセスを実践する。第8章のデモとして使用する。

### A3. 成功基準

- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_yaml.sh全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

### A4. やらないこと（スコープ外）

- 5基準スコアリング（エッジの重み計算は行わない）
- 可視化（HTMLグラフの生成は本プロジェクトのスコープ外）
- 論文の内容に対する学術的評価

### A5. 品質の優先順位

1. スキーマ準拠（構造的整合性）
2. 概念の網羅性（各論文の主要概念が抽出されていること）
3. 統合の整合性（論文間の関係が適切にエッジ化されていること）

### A6. 成果物の用途

- 利用者: 講義ノート（第8章）の読者
- 用途: 反復サイクルによるHarness改善の実例として参照
- 閲覧環境: GitHub上のexamplesディレクトリ、または講義ノート本文

---

## B. データに関する決定

### B1. データソース一覧

| # | ファイル | 種別 | 論文 | 備考 |
|---|---------|------|------|------|
| 1 | input/science.adt2760.pdf | 論文PDF | Gianni et al. (2026) Science — QT45リボザイムによるRNA自己複製 | 第7章でも使用 |
| 2 | input/s41559-024-02461-1.pdf | 論文PDF | Moody et al. (2024) Nature Ecology & Evolution — LUCAのゲノム再構成と年代推定 | |
| 3 | input/s00239-009-9270-1.pdf | 論文PDF | Yarus et al. (2009) Journal of Molecular Evolution — 遺伝暗号の起源と立体化学仮説 | |

### B2. データ補充方針

- 補充の要否: 不要
- 3本の論文のみを入力とする。外部情報の検索・補充は行わない。

### B3. 収束条件

- 条件1: 各論文から15ノード以上が抽出されていること
- 条件2: 各論文から15エッジ以上が抽出されていること
- 条件3: 統合YAMLに論文間をつなぐエッジが1本以上存在すること

### B4. 不確実性の許容レベル

- 判読不能: PDF内の図表キャプション等は省略可。本文テキストが読めれば可。
- 信頼度「低」のソース: なし（査読済み論文のみ）
- 要確認箇所: なし

### B5. 表記ルール

- 言語: 日本語（ノードのlabel、description）
- 人名: 論文のfirst authorの姓（例: Gianni, Moody, Yarus）
- 専門用語: 英語の専門用語はそのまま使用可（例: RNA World、リボザイム）
- ノードID命名規則:
  - snake_caseで記述する
  - 英語表記で統一する（日本語をローマ字にしない）
  - 概念の最も一般的な名称を使う（例: `rna_world` ✅、`rna_world_hypothesis` ❌）
  - 下記の共通ノードseed listに該当する概念は、**必ず指定されたIDを使用する**

**共通ノード seed list（全Workerが使用すること）**:

以下のノードは3本の論文にまたがって登場する可能性がある概念である。
該当する概念が論文中に登場した場合、以下のIDとtypeを使用すること。
論文固有の詳細はdescriptionに記述する。

| id | label | type | 該当する論文 |
|----|-------|------|-------------|
| `rna_world` | RNAワールド | concept | Gianni, Yarus（Moodyでも言及があれば使用） |
| `luca` | LUCA（全生物最終共通祖先） | concept | Moody（Gianni, Yarusでも言及があれば使用） |
| `genetic_code` | 遺伝暗号 | concept | Yarus（Moodyでも言及があれば使用） |
| `in_vitro_selection` | in vitro選択 | method | Gianni, Yarus |
| `prebiotic_chemistry` | プレバイオティック化学 | concept | Gianni, Moody（Yarusでも言及があれば使用） |
| `rna_self_replication` | RNA自己複製 | process | Gianni（Yarusでも言及があれば使用） |

seed listに含まれない概念のIDは、Worker（Claude）が上記の命名規則に従って自由に決定してよい。

### B6. ドメイン知識

- 略語・専門用語の定義:
  - LUCA: Last Universal Common Ancestor（全生物の最終共通祖先）
  - RNA World: RNAが遺伝情報と触媒機能の両方を担っていたとする仮説
  - リボザイム: 触媒活性を持つRNA分子
- 読み方が特殊な用語: なし
- ドメイン固有の分類体系: なし

---

## C. 構造化に関する決定

### C1. ノード粒度

- 方針: 各論文の主要な概念・分子・プロセス・手法をノードとする。第7章（Gianni論文）の粒度を踏襲。
- 具体例:
  - ノードにする: RNAワールド仮説、QT45リボザイム、LUCA、立体化学仮説、RNA自己複製
  - ノードにしない（属性として扱う）: 著者名、出版年、DOI、具体的な数値（収率、忠実度の値）

### C2. 期待するグラフ規模

- ノード数の目安: 個別 15〜30 × 3本 → 統合後 50〜70（重複マージ後）
- エッジ数の目安: 個別 15〜30 × 3本 → 統合後 60〜100（論文間エッジ含む）

### C3. 重視する関係の種類

- 最重要: supports（仮説の支持関係）、derives（理論の導出関係）
- 重要: causes（因果関係）、requires（前提条件）
- あれば記録: contains, compares, produces, inhibits

### C4. エッジの閾値方針

- 方針: 全ペア（明示的に関連するもののみ）
- 閾値: なし（5基準スコアリングを行わないため）
- 潜在的関係: 記録しない

### C5. 5基準スコアのキャリブレーション

なし（本プロジェクトでは5基準スコアリングを行わない）

### C6. 参照実装

第7章の最終出力（examples/chapter7/output/science_adt2760.yaml）のスキーマを踏襲する。具体的な仕様は以下の通り:

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

---

## D. 実装に関する決定

### D1. 入出力

- 入力:
  - ファイル: input/science.adt2760.pdf, input/s41559-024-02461-1.pdf, input/s00239-009-9270-1.pdf
  - 形式: PDF
- 出力:
  - 個別YAML: output/gianni.yaml, output/moody.yaml, output/yarus.yaml
  - 統合YAML: output/merged.yaml
  - 形式: YAML（C6のスキーマに準拠）
  - 配置場所: output/

### D2. 技術スタック

- 言語: Python 3.x（検証スクリプト、マージスクリプト）
- ライブラリ: PyYAML（YAML解析）
- 制約: なし

### D3. Phase構成の方針

- Phase構成: 以下の構成を指定

| Phase | 内容 | 担当 |
|-------|------|------|
| Phase 1 | Gianni論文の概念抽出・YAML生成 | Worker A |
| Phase 2 | Moody論文の概念抽出・YAML生成 | Worker B |
| Phase 3 | Yarus論文の概念抽出・YAML生成 | Worker C |
| Phase 4 | 個別YAMLのマージ・論文間エッジ追加 | Lead（merge.pyを使用） |

Phase 1〜3は独立に実行可能。Phase 4はPhase 1〜3の完了後に実行する。

### D4. エージェント構成

- モード: エージェントモード
- 分離方針: 論文ごとにWorkerを分離する
- 理由: 各論文のコンテキストが独立しており、Worker間のコンテキスト汚染を防ぐため。1セッションで3本を逐次処理すると、3本目の処理時に前の論文の情報がコンテキストを圧迫する。

| agent_id | 役割 | 担当Phase | 入力 | 出力 |
|----------|------|----------|------|------|
| worker_gianni | Gianni論文の概念抽出 | Phase 1 | input/science.adt2760.pdf | output/gianni.yaml |
| worker_moody | Moody論文の概念抽出 | Phase 2 | input/s41559-024-02461-1.pdf | output/moody.yaml |
| worker_yarus | Yarus論文の概念抽出 | Phase 3 | input/s00239-009-9270-1.pdf | output/yarus.yaml |

- parallel_workers: 3
- 並列化の理由: 3本の論文は入力・出力ともに独立しており、Worker間の依存関係がない。並列実行により処理時間を短縮できる。
- chunkwiseモード関連: なし（論文ごとの分離であり、チャンク分割ではない）

### D5. 検証方法

検証は2段階で実施する。

**第1段階: 個別YAML検証（各Worker完了時）**
- validate_yaml.sh による9項目チェック（第7章と同一）:
  1. output/ にYAMLファイルが存在するか
  2. nodesセクションが存在するか
  3. edgesセクションが存在するか
  4. ノードが1個以上あるか
  5. エッジが1個以上あるか
  6. エッジのsource/targetがnodesのIDに存在するか
  7. 孤立ノード（どのエッジからも参照されないノード）がないか
  8. typeが許可リスト7種に含まれるか
  9. relationが許可リスト8種に含まれるか

**第2段階: 統合YAML検証（マージ後）**
- 上記9項目に加えて:
  10. 3本すべての論文由来のノードが含まれていること（metadataのdoiで確認）

### D6. マージ方針

- マージツール: merge.py（exact-matchによるノードデデュプリケーション）
- マージ手順:
  1. 3本の個別YAMLを読み込む
  2. ノードIDが完全一致するものを統合（exact-match）
  3. 全エッジを統合
  4. 論文間をまたぐエッジをLeadが追加（Claude判断可: 明示的に関連するもののみ）
  5. 統合YAMLをoutput/merged.yamlに出力

---

## E. 経験と判断

### E1. 関連する過去の経験

- 第7章でGianni論文を4段階で構造化した経験がある
- v19ワークフローでAgentsモード（Lead-Worker構造）を運用した経験がある
- merge.pyによるexact-matchデデュプリケーションの実績がある
- **サイクル1の実行結果**: 命名規則なしで実行したところ、63ノード中exact-matchしたのは1件（`in_vitro_selection`）のみ。同一概念（RNAワールド）に `rna_world_hypothesis`（Gianni）と `rna_world`（Yarus）が振られ、統合YAMLに重複ノードが残存した。

### E2. 予想されるリスク

| リスク | 影響 | 対処方針 |
|--------|------|---------|
| ~~同じ概念に異なるノードIDが振られる~~ | ~~マージ時の重複ノード残存~~ | **サイクル1で発生を確認 → B5にseed listを追加して対処済み** |
| PDF読み取りの品質差 | 論文によって抽出精度が異なる | 個別YAMLの成功基準（B3）で最低ラインを担保 |
| Worker間で粒度が揃わない | 統合後のネットワークがアンバランスになる | 個別YAMLのレビューで調整 |
| seed list以外の概念で命名が揺れる | 一部の重複が残る可能性 | satisficingの範囲内として許容する |

### E3. 人間が判断すべきポイント

| タイミング | 確認内容 | 判断基準 |
|-----------|---------|---------|
| Phase 1〜3完了後 | 個別YAMLの概念抽出が妥当か | ノード数・エッジ数がB3の基準を満たし、主要概念が含まれているか |
| Phase 1〜3完了後 | seed listのIDが正しく使われているか | 共通概念にseed listのIDが振られているか |
| Phase 4完了後 | 統合YAMLの品質 | 論文間エッジが存在し、重複ノードが過度でないか |
| サイクル終了判断 | satisficing基準 | A3の成功基準をすべて満たしているか |

### E4. 設計上の選択理由

| 選択 | 理由 | 却下した代替案 |
|------|------|--------------|
| 論文ごとにWorkerを分離 | コンテキスト汚染の防止 | 1セッションで逐次処理（コンテキスト圧迫のリスク） |
| merge.pyでexact-match | シンプルで確実 | LLMによるセマンティックマッチング（精度不確実） |
| 5基準スコアリングなし | デモの焦点は反復サイクルであり、スコアリング精度ではない | 5基準あり（複雑さが増しデモの焦点がぼやける） |
| **seed listで上流統一** | **Worker定義に共通IDを渡すことでmerge.pyの変更不要** | **merge.pyにファジーマッチを追加（スクリプト変更が必要、精度不確実）** |

---

## F. 学術ペルソナ定義

なし（本プロジェクトではペルソナレビューは実施しない）
