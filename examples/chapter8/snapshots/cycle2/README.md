# Cycle 2 — proposal.md v1.1 修正と再実行

## サイクル1で発見された問題

### 問題の概要

3つのWorkerが独立にYAMLを生成した結果、同じ概念に異なるノードIDが振られた。merge.pyのexact-matchでは63ノード中1件（`in_vitro_selection`）しかマッチせず、統合後に62ノードが残った（理想的には50〜70に圧縮されるはず）。

### 最も象徴的な事例

| Worker | ノードID | label |
|--------|---------|-------|
| Gianni | `rna_world_hypothesis` | RNAワールド仮説 |
| Yarus | `rna_world` | RNAワールド |

同一概念に対してGianniは「仮説」を含むID、Yarusは含まないIDを採用。Leadはマージ時にこの2つの間に `supports` エッジを張った——本来同一ノードであるべきものが「支持関係」として接続されている。

### GianniとMoodyの間にexact-matchがゼロ

生命の起源という共通テーマにもかかわらず、2つのWorker間で一致するIDが1つもなかった。

### 8.1のサイクル図に照らした判断

この問題は**仕様レベル**に起因する。Worker個別の実装は正しく動いている（スキーマ準拠、孤立ノードなし、収束条件クリア）。問題は、proposal.mdにノード命名規則を書かなかったこと。

→ **意図の表明（proposal.md）に戻って修正する**

---

## proposal.md v1.0 → v1.1 の変更内容

### 変更箇所1: B5（表記ルール）にノードID命名規則を追加

**変更前**:
```
- その他の統一ルール: なし
```

**変更後**:
```
- ノードID命名規則:
  - snake_caseで記述する
  - 英語表記で統一する（日本語をローマ字にしない）
  - 概念の最も一般的な名称を使う（例: rna_world ✅、rna_world_hypothesis ❌）
  - 下記の共通ノードseed listに該当する概念は、必ず指定されたIDを使用する
```

**変更理由**: Workerに命名の自由度を完全に委ねた結果、同じ概念に異なるIDが振られた。命名規則を仕様で統一することで、merge.pyの変更なしに上流で問題を解決する。

### 変更箇所2: B5に共通ノードseed listを追加

**追加内容**:

| id | label | type | 該当する論文 |
|----|-------|------|-------------|
| `rna_world` | RNAワールド | concept | Gianni, Yarus |
| `luca` | LUCA（全生物最終共通祖先） | concept | Moody |
| `genetic_code` | 遺伝暗号 | concept | Yarus |
| `in_vitro_selection` | in vitro選択 | method | Gianni, Yarus |
| `prebiotic_chemistry` | プレバイオティック化学 | concept | Gianni, Moody |
| `rna_self_replication` | RNA自己複製 | process | Gianni |

**変更理由**: サイクル1の結果から、3論文にまたがって登場する概念を特定した。これらの共通概念に固定IDを割り当てることで、Workerが独立に処理しても同一概念には同一IDが使われる。seed listに含まれない論文固有の概念は、Workerが命名規則に従って自由に命名する。

**設計判断**: merge.pyにファジーマッチを追加する案も検討したが、却下した。理由は2つ。第一に、スクリプト変更が不要で、proposal.mdの修正だけで解決できる。第二に、ファジーマッチの精度が不確実で、誤マッチのリスクがある。「上流（仕様）で統一する」方が「下流（スクリプト）で吸収する」よりシンプルで確実。

### 変更箇所3: E1（過去の経験）にサイクル1の結果を追記

**追加内容**: 「サイクル1の実行結果: 命名規則なしで実行したところ、63ノード中exact-matchしたのは1件のみ」

**変更理由**: 次にこのproposal.mdを読む人（別セッション、別のClaude instance）が、なぜseed listが必要かを理解できるようにする。

### 変更箇所4: E2（リスク）とE4（設計上の選択理由）を更新

- E2: 命名リスクを「発生確認→対処済み」に更新。seed list以外の概念で揺れが残るリスクを新規追加（satisficingの範囲内として許容）。
- E4: seed listで上流統一する選択とその理由を追加。

---

## 変更しなかったこと

- **A3（成功基準）**: 変更なし。成功基準自体は妥当だった。問題は基準を満たすための仕様が不十分だったこと。
- **D3（Phase構成）**: 変更なし。Worker分離の方針は正しかった。
- **D5（検証方法）**: 変更なし。validate_phase.pyの10項目チェックは構造的整合性を正しく検証した。命名の意味的一貫性は検証スクリプトの範囲外であり、仕様（proposal.md）で対処すべき問題。
- **D6（マージ方針）**: 変更なし。merge.pyのexact-matchはseed listと組み合わせれば十分に機能する。

---

## /setup 再実行の結果（v1.1）

### spec.md の変更

バージョン履歴が更新された:
- v1.0: `superseded`（初期実装）
- v1.1: `active`（seed list追加。サイクル1の命名揺れ対策）

spec.mdの「表記ルール」セクションに以下が追加された:
- ノードID命名規則（3項目）
- 共通ノードseed list（6概念のテーブル）

### Worker定義の変更

3体のWorker定義すべてに以下が追加された:

**新規セクション「ノードID命名規則」**（★重要★マーカー付き）:
- snake_case、英語統一、最も一般的な名称を使う、の3ルール
- seed listに該当する概念は必ず指定IDを使用する指示

**新規セクション「共通ノード seed list」**（★必ず使用すること★マーカー付き）:
- 6概念のテーブル
- 論文ごとに「✅ 該当する場合は必ず使用」と「言及があれば使用」を区別
  - 例: worker_gianniでは `rna_world` と `in_vitro_selection` が ✅、`luca` は「言及があれば」
  - 例: worker_moodyでは `luca` と `prebiotic_chemistry` が ✅、`rna_world` は「言及があれば」

**完了条件に追加**: 「seed listに該当する概念が指定IDで登録されている」

**タスク一覧の更新**: 「ノードとエッジを定義する（seed listのIDを優先使用）」

### 変更されなかったファイル

- **merge.py**: ロジック変更なし（意図通り）。seed listにより入力側が統一されるため不要。
- **validate_phase.py**: 検証項目の追加なし。
- **settings.json**: Hooks構成の変更なし。

---

## /execute 実行結果（サイクル2）

### 全体サマリー

| Phase | Worker | ノード数 | エッジ数 | 検証（第1層）| commit |
|-------|--------|---------|---------|------------|--------|
| 1 | worker_gianni | 20 | 21 | PASS | 4caf800 |
| 2 | worker_moody | 21 | 21 | PASS | dc6d93a |
| 3 | worker_yarus | 22 | 21 | PASS | 0d893bf |
| 4 | Lead（マージ）| 60 | 68 | PASS（10項目）| — |

- Worker 3体は並列起動
- 全Phaseで第1層検証 PASS
- 成功基準: 4項目すべて PASS
- Stop Hook機能: progress.md更新 + git commit が各Phaseで強制された ✅

### seed list の遵守状況

| seed ID | Gianni | Moody | Yarus | マージでexact-match |
|---------|--------|-------|-------|-------------------|
| `rna_world` | ✅ | — | ✅ | ✅ 統合された |
| `luca` | — | ✅ | — | — (単独) |
| `genetic_code` | — | — | ✅ | — (単独) |
| `in_vitro_selection` | ✅ | — | ✅ | ✅ 統合された |
| `prebiotic_chemistry` | ✅ | ✅ | — | ✅ 統合された |
| `rna_self_replication` | ✅ | — | — | — (単独) |

6個中6個がWorkerに使用された。3個（rna_world, in_vitro_selection, prebiotic_chemistry）が2論文以上で共有され、merge.pyのexact-matchで正しく統合された。

### RNA World 命名問題の解決

| | サイクル1 | サイクル2 |
|--|---------|---------|
| Gianni | `rna_world_hypothesis` | `rna_world` ✅ |
| Yarus | `rna_world` | `rna_world` ✅ |
| マージ結果 | 2ノード（重複残存）| 1ノード（正しく統合）|

**サイクル1でLeadが張った偽のエッジ**（`rna_world_hypothesis --[supports]--> rna_world`）**が消滅**。同一ノードとして正しく統合された。

### 残存する命名の揺れ

label（表示名）レベルでの意味的重複チェック: **検出なし**。
seed list以外の概念でも命名規則（snake_case、英語統一、最も一般的な名称）が効いている。

---

## サイクル1 → サイクル2 の比較

### 数値比較

| 指標 | サイクル1 | サイクル2 | 変化 |
|------|---------|---------|------|
| 個別YAML合計ノード | 63 | 63 | ±0 |
| 個別YAML合計エッジ | 66 | 63 | -3 |
| exact-matchしたノード | 1 | 3 | **+2** |
| 統合後ノード | 62 | 60 | **-2** |
| 統合後エッジ（マージ直後） | 66 | 63 | -3 |
| 論文間エッジ（Lead追加） | 5 | 5 | ±0 |
| 統合後エッジ（最終） | 71 | 68 | -3 |
| 論文間の自然な接続 | 7 | 11 | **+4** |
| 重複RNA Worldノード | 2 | 1 | **解決** |
| 命名の意味的衝突 | あり | なし | **解決** |

### 質的な改善

**論文間接続の質が向上**。サイクル1ではLeadが追加した5本の論文間エッジのうち1本が偽のエッジ（rna_world_hypothesis → rna_world）だった。サイクル2では偽のエッジが消え、代わりに共有ノードを介した自然な接続が増えた（7本 → 11本）。

主な論文間接続:
- `rna_world` (G/Y) → `rna_self_replication` (G): RNAワールドはRNA自己複製を前提とする
- `rna_world` (G/Y) → `drt_model` (Y): RNAワールドがDRTモデルを支持
- `luca` (M) → `prebiotic_chemistry` (G/M): LUCAからプレバイオティック化学が導出される
- `luca` (M) → `genetic_code` (Y): LUCAが遺伝暗号を含む
- `prebiotic_chemistry` (G/M) ← `hydrothermal_environment` (M): 熱水環境がプレバイオティック化学を支持

共有ノードがハブとして論文間を接続する構造が自然に生まれている。

---

## Satisficing 判断

### A3 成功基準との照合

- 基準1: 3本すべての論文が個別にYAML化 ✅
- 基準2: 個別YAMLがスキーマ準拠（validate_phase.py PASS）✅
- 基準3: 統合YAMLが生成・スキーマ準拠（validate_phase.py --final PASS）✅
- 基準4: 統合YAMLに3本すべてのDOI含む ✅

### 残存リスクの評価

seed list以外の概念での命名揺れ: **検出なし**。命名規則（snake_case、英語統一、最も一般的な名称）が確率的制御として十分に機能した。

### 結論

**サイクル2で完了とする**。成功基準4項目すべてPASS。命名問題はseed listで解決し、残存する揺れも検出されなかった。これ以上のサイクルは8.5（satisficing）の原則に基づき不要と判断する。

---

## 8.1〜8.5 の原理がどこに現れたか

| 原理 | 本サイクルでの具体例 |
|------|-------------------|
| **8.1 反復サイクル** | サイクル1で問題発見 → 仕様に戻る → サイクル2で改善 |
| **8.2 意図の文書化** | proposal.mdにseed listを追加。変更履歴に理由を明記 |
| **8.3 構造化** | proposal.md v1.1 → /setup → spec.md + Worker定義に自動波及 |
| **8.4 外部永続化** | Stop Hookがprogress.md更新とgit commitを強制。snapshotsに各サイクルの記録を保存 |
| **8.5 Satisficing** | 成功基準4項目PASSで完了判断。seed list外の揺れはsatisficingの範囲内 |
