# Codex CLI 段階2 — AGENTS.md + Rules

実行日: 2026-03-15
構成: AGENTS.md（Rules統合版）。type 7種・relation 8種の許可リスト追加。Skillsなし。
入力: science.adt2760.pdf（Gianni et al., Science 2026）

## 出力の概要

| 指標 | Codex 段階1 | Codex 段階2 | 変化 |
|------|-------------|-------------|------|
| ノード数 | 16 | 18 | +2 |
| エッジ数 | 18 | 21 | +3 |
| type種数 | 7/7 | 7/7 | 不変 |
| relation種数 | 7/8 | 6/8 | -1（derives消失） |
| 概要把握コメント | あり（自発） | あり（自発） | 不変 |

## 段階1の予測の検証

段階1で「CodexにRulesを追加してもほぼ変わらない」と予測した。結果は**ノード+2、ほぼ安定**。予測は正しかった。

## Rulesが「確認」として作用した証拠

type 7種の使用は段階1と段階2で完全に同一（7/7）。Rulesの追加前と追加後で変わらない。これはRulesが「新しい制約を加えた」のではなく「既存のデフォルトを確認した」だけであることを裏付ける。

## 微細な変化: type再分類

Rulesが「教科書的な語彙の確認」として作用した結果、いくつかのノードでtype再分類が起きた:

| 段階1 | 段階2 | 変化 |
|-------|-------|------|
| pppauugau_hexamer (entity) | hexamer_supplementation (method) | 物質→手法に再解釈 |
| — | error_threshold_model (method) | アイゲン閾値が新たにmethod扱いで追加 |
| small_size_45nt (property) | — | 消失（large_size_complexityに統合？） |
| — | large_size_complexity (property) | 新規追加 |

特にヘキサマーが entity → method に変わったのは注目に値する。段階1ではヘキサマーを「物質」として捉えていたが、Rulesのmethod定義（「手法・技術・実験手順」）を読んだことで「手法」として再解釈した。Rulesは新しい制約ではなく、分類判断のキャリブレーションとして作用した。

## relation の微変化

| relation | 段階1 | 段階2 | 変化 |
|----------|-------|-------|------|
| supports | 4 | 6 | +2 |
| produces | 5 | 5 | 不変 |
| inhibits | 2 | 3 | +1 |
| causes | 3 | 2 | -1 |
| derives | 2 | 0 | **消失** |
| requires | 1 | 1 | 不変 |
| contains | 1 | 1 | 不変 |
| compares | 0 | 0 | 依然不使用 |

derivesが消失した。段階1では `random_rna_sequence_pool → qt45_ribozyme` と `in_vitro_selection → qt45_ribozyme` にderivesを使っていたが、段階2では同じ関係に produces を使った。Rulesに derives の定義「AからBが派生する」を読んだ結果、「発見」の関係はderivesよりproducesが適切だと判断を変えた可能性がある。

## 三ツール段階2の比較

| | Claude | Codex | Gemini |
|---|---|---|---|
| 段階1 | 22 | 16 | 11 |
| 段階2 | 27 | 18 | 9 |
| 変化 | +5 | +2 | **-2** |

三ツールの変化方向が明確に分かれた:
- **Claude (+5)**: Rulesのtype定義が「探索の方向性」を与え、ノードが増えた。「method」「problem」の定義を読んで、該当するノードを積極的に探したと推測。
- **Codex (+2)**: デフォルト語彙がRulesと一致しているため、微調整のみ。
- **Gemini (-2)**: Rulesが「制限」として作用し、ノードが減った。段階1にあったspontaneous_emergence, replication_fidelityが消失。

## Rulesの機能がモデルで質的に異なることの確認

段階1の仮説がデータで裏付けられた:
- **Claudeに対して**: Rulesは「自由な発明を方向づける探索ガイド」
- **Codexに対して**: Rulesは「デフォルト語彙の確認と分類のキャリブレーション」
- **Geminiに対して**: Rulesは「ノードを絞り込む制限」＋「relation語彙を教える教育」（段階1でcauses不使用→段階2で2件使用）
