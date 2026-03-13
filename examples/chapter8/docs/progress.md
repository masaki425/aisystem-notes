# 進捗管理

## プロジェクトの目的（常に意識すること）
第7章では論文1本の概念構造化を行い、CLAUDE.md → Rules → Skills → Hooks の4段階でHarnessの効果を観察した。本プロジェクトでは入力を3本に拡張し、反復サイクルを通じてHarness設計を改善するプロセスを実践する。第8章のデモとして使用する。

## 成功基準（常に意識すること）
- 基準1: 3本すべての論文が個別にYAML化されていること
- 基準2: 個別YAMLがスキーマに準拠していること（validate_phase.py全項目合格）
- 基準3: 統合YAMLが生成され、スキーマに準拠していること
- 基準4: 統合YAMLに3本すべての論文由来のノードが含まれていること

## 現在の状態
- spec_version: 1.1
- execution_mode: agent
- current_phase: 1
- current_task: 1.1
- status: not_started
- last_completed_task: none
- blocked_by: none

## 次にやること
1. CLAUDE.md を読む
2. docs/spec.md を読む
3. Phase 1〜3 の Worker を Taskツールで同時起動する

## タスク一覧
- [ ] 1.1: Gianni論文を読み込み、主要概念を抽出する
- [ ] 1.2: ノードとエッジを定義し、output/gianni.yaml を生成する
- [ ] 1.3: スキーマ準拠を確認する（validate_phase.py --phase 1）
- [ ] 2.1: Moody論文を読み込み、主要概念を抽出する
- [ ] 2.2: ノードとエッジを定義し、output/moody.yaml を生成する
- [ ] 2.3: スキーマ準拠を確認する（validate_phase.py --phase 2）
- [ ] 3.1: Yarus論文を読み込み、主要概念を抽出する
- [ ] 3.2: ノードとエッジを定義し、output/yarus.yaml を生成する
- [ ] 3.3: スキーマ準拠を確認する（validate_phase.py --phase 3）
- [ ] 4.1: 3本の個別YAMLを読み込み、merge.py でマージする
- [ ] 4.2: 論文間をまたぐエッジをLeadが追加する
- [ ] 4.3: 統合YAMLの検証（validate_phase.py --final）

## 検証結果
| Phase | 検証日時 | 自動検証（第1層） | 自動レビュー（第2層） | 手動検証 | 成功基準との照合 | commit |
|-------|----------|-------------------|----------------------|----------|------------------|--------|
| 1     |          |                   |                      |          |                  |        |
| 2     |          |                   |                      |          |                  |        |
| 3     |          |                   |                      |          |                  |        |
| final |          |                   |                      |          |                  |        |

## エージェント実行状況
| エントリ | worker_gianni | worker_moody | worker_yarus | Phase 4（Lead） | 最終検証 |
|----------|---------------|--------------|--------------|-----------------|----------|
| main     | ⬜ 未実行     | ⬜ 未実行    | ⬜ 未実行    | ⬜ 未実行       | ⬜       |

※ ステータス: ⬜ 未実行 / 🔄 実行中 / ✅ PASS / ❌ FAIL / ⚠️ スキップ

## 作業ログ
（タスク完了ごとに追記）
