# Gemini CLI 移植テスト

第7章の段階4 Harness（Claude Code）を Gemini CLI に移植した構成。

## 変換内容

### 第1層（ドキュメント層）
変換なし。自然言語で書かれた指示はそのまま読める。

### 第2層（実行環境層）

| Claude Code | Gemini CLI | 変換内容 |
|-------------|------------|---------|
| `CLAUDE.md` | `GEMINI.md` | リネーム + Rules統合 |
| `.claude/rules/structurize.md` | （GEMINI.mdに統合） | Geminiは独立Rulesファイル非対応 |
| `.claude/skills/structurize/SKILL.md` | `.gemini/skills/structurize/SKILL.md` | パス変更のみ（SKILL.md標準フォーマット） |
| `scripts/validate_yaml.sh` | `scripts/validate_yaml.sh` | 変換不要（決定論的コード） |

### 第3層（手順保証層）

| Claude Code | Gemini CLI | 差異 |
|-------------|------------|------|
| `.claude/settings.json` Stop hook | `.gemini/settings.json` AfterAgent | ほぼ等価。失敗時にエージェントに差し戻す |
| PreToolUse hook（未使用） | BeforeTool（利用可能） | Geminiにも実行前ブロック機構がある |
| — | `gemini hooks migrate --from-claude` | Claude Code設定からの自動移行コマンドが存在 |

## Claude Code との第3層の比較

Gemini CLIはClaude Codeとほぼ同等のHooks機構を備えている。

- **AfterAgent** = Claude CodeのStop hook。エージェント完了後にスクリプトを実行し、失敗なら差し戻す
- **BeforeTool** = Claude CodeのPreToolUse hook。ツール実行前にブロック可能
- **BeforeModel** = Claude Codeにない機能。LLMリクエスト自体を修正できる
- **Checkpointing（/restore）** = ファイル変更前の自動スナップショット。Claude Codeにはない安全網

今回の移植テストではAfterAgentのみ使用し、BeforeToolは使わない（Claude Code側でもPreToolUseは未使用のため、条件を揃える）。

## 観察ポイント

1. **SKILL.md の解釈**: Geminiモデルが同じSKILL.mdの手順をどの順序で実行するか
2. **Rules の遵守**: GEMINI.mdに統合した7種type・8種relationの制約が守られるか
3. **Hooks の強制力**: AfterAgentがvalidate_yaml.shの失敗に基づいて差し戻すか（Claude CodeのStop hookとの等価性）
4. **孤立ノード**: 第7章で段階3まで残り続けた `ribozyme_abundance` 相当の問題が、Hooksで解決されるか
5. **migrate コマンドの精度**: `gemini hooks migrate --from-claude` で自動変換した場合と手動変換した場合の差異

## 実行方法

```bash
# 1. 入力PDFをコピー
cp ../../../chapter7/input/science.adt2760.pdf input/

# 2. スクリプトに実行権限を付与
chmod +x scripts/validate_yaml.sh

# 3. Gemini CLI で実行
gemini "GEMINI.mdを読み、.gemini/skills/structurize/SKILL.mdに従って論文を構造化してください"
```

## 補足: migrate コマンドによる自動変換（参考）

```bash
# Claude Code の設定から Gemini CLI 設定を自動生成する場合
cd ../../../chapter7
gemini hooks migrate --from-claude
# → .gemini/settings.json が自動生成される
```

この自動変換の精度と、手動変換（本ディレクトリの構成）との差異も観察対象とする。
