# 進捗管理

## プロジェクトの目的（常に意識すること）
第7章では論文1本の概念構造化を行い、CLAUDE.md → Rules → Skills → Hooks の4段階でHarnessの効果を観察した。本プロジェクトでは入力を3本に拡張し、反復サイクルを通じてHarness設計を改善するプロセスを実践する。第8章のデモとして使用する。

## 成功基準（常に意識すること）
- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_phase.py全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

## 現在の状態
- spec_version: 1.3
- execution_mode: agent
- current_phase: 1
- current_task: 1.1
- status: not_started
- last_completed_task: none
- blocked_by: none

## 次にやること
1. CLAUDE.md を読む
2. docs/spec.md を読む
3. Phase 1〜3 を並列実行: worker_gianni, worker_moody, worker_yarus を Task ツールで同時起動
4. Phase 4: merge.py で統合 + 論文間エッジ追加
5. 最終検証: validate_phase.py --final

## タスク一覧
- [ ] 1.1: Gianni論文の概念ノード抽出
- [ ] 1.2: Gianni論文のエッジ抽出
- [ ] 1.3: output/gianni.yaml 生成
- [ ] 1.4: validate_phase.py --phase 1
- [ ] 2.1: Moody論文の概念ノード抽出
- [ ] 2.2: Moody論文のエッジ抽出
- [ ] 2.3: output/moody.yaml 生成
- [ ] 2.4: validate_phase.py --phase 2
- [ ] 3.1: Yarus論文の概念ノード抽出
- [ ] 3.2: Yarus論文のエッジ抽出
- [ ] 3.3: output/yarus.yaml 生成
- [ ] 3.4: validate_phase.py --phase 3
- [ ] 4.1: merge.py で統合
- [ ] 4.2: 論文間エッジ追加
- [ ] 4.3: output/merged.yaml 生成
- [ ] 4.4: validate_phase.py --final

## 検証結果
| Phase | 検証日時 | 自動検証（第1層） | 自動レビュー（第2層） | 手動検証 | 成功基準との照合 | commit |
|-------|----------|-------------------|----------------------|----------|------------------|--------|
| 1     |          |                   |                      |          |                  |        |
| 2     |          |                   |                      |          |                  |        |
| 3     |          |                   |                      |          |                  |        |
| final |          |                   |                      |          |                  |        |

## エージェント実行状況
| worker_gianni | worker_moody | worker_yarus | Phase 4 (Lead) | 最終検証 |
|---------------|--------------|--------------|----------------|----------|
| ⬜ 未実行 | ⬜ 未実行 | ⬜ 未実行 | ⬜ 未実行 | ⬜ |

※ ステータス: ⬜ 未実行 / 🔄 実行中 / ✅ PASS / ❌ FAIL / ⚠️ スキップ

## 作業ログ
### 2026-03-13 /setup 実行
- proposal.md v1.3 から spec.md v1.3 を生成（サイクル4）
- v1.3 の主な変更: D5の検証方法にB3条件3・4のスクリプト検証を追加
