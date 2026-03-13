# 進捗管理

## プロジェクトの目的（常に意識すること）
第7章では論文1本の概念構造化を行い、CLAUDE.md → Rules → Skills → Hooks の4段階でHarnessの効果を観察した。本プロジェクトでは入力を3本に拡張し、反復サイクルを通じてHarness設計を改善するプロセスを実践する。第8章のデモとして使用する。

## 成功基準（常に意識すること）
- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_phase.py全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

## 現在の状態
- spec_version: 1.2
- execution_mode: agent
- current_phase: 1
- current_task: 1.1
- status: not_started
- last_completed_task: none
- blocked_by: none

## 次にやること
1. CLAUDE.md を読む
2. docs/spec.md を読む
3. Phase 1〜3 の Worker を並列起動（worker_gianni, worker_moody, worker_yarus）
4. 全 Worker 完了後、Phase 4（merge.py + 論文間エッジ追加）を実行

## タスク一覧
- [ ] 1.1: Gianni論文の概念抽出（worker_gianni）
- [ ] 1.2: output/gianni.yaml 生成
- [ ] 1.3: validate_phase.py --phase 1
- [ ] 2.1: Moody論文の概念抽出（worker_moody）
- [ ] 2.2: output/moody.yaml 生成
- [ ] 2.3: validate_phase.py --phase 2
- [ ] 3.1: Yarus論文の概念抽出（worker_yarus）
- [ ] 3.2: output/yarus.yaml 生成
- [ ] 3.3: validate_phase.py --phase 3
- [ ] 4.1: merge.py で3本の個別YAMLをマージ
- [ ] 4.2: 論文間エッジを追加
- [ ] 4.3: validate_phase.py --final

## 検証結果
| Phase | 検証日時 | 自動検証（第1層） | 自動レビュー（第2層） | 手動検証 | 成功基準との照合 | commit |
|-------|----------|-------------------|----------------------|----------|------------------|--------|
| 1     |          |                   |                      |          |                  |        |
| 2     |          |                   |                      |          |                  |        |
| 3     |          |                   |                      |          |                  |        |
| 4     |          |                   |                      |          |                  |        |

## エージェント実行状況
| エントリ | worker_gianni | worker_moody | worker_yarus | Phase 4（Lead） | 最終検証 |
|----------|---------------|--------------|--------------|-----------------|----------|
| default  | ⬜ 未実行      | ⬜ 未実行     | ⬜ 未実行     | ⬜ 未実行        | ⬜       |

※ ステータス: ⬜ 未実行 / 🔄 実行中 / ✅ PASS / ❌ FAIL / ⚠️ スキップ

## 作業ログ

### 2026-03-13 /setup（サイクル3）
- proposal.md v1.2 から spec.md v1.2 を生成
- v1.2 の変更点: 収束条件強化（論文間エッジ各ペア2本以上）、seed list運用ルール厳格化（Moodyにrna_world/genetic_code必須化）
