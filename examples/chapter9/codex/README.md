# Codex CLI 移植テスト

第7章の段階4 Harness（Claude Code）を Codex CLI に移植した構成。

## 変換内容

### 第1層（ドキュメント層）
変換なし。自然言語で書かれた指示はそのまま読める。

### 第2層（実行環境層）

| Claude Code | Codex CLI | 変換内容 |
|-------------|-----------|---------|
| `CLAUDE.md` | `AGENTS.md` | リネーム + Rules統合 |
| `.claude/rules/structurize.md` | （AGENTS.mdに統合） | Codexは独立Rulesファイル非対応 |
| `.claude/skills/structurize/SKILL.md` | `.agents/skills/structurize/SKILL.md` | パス変更のみ（SKILL.md標準フォーマット） |
| `scripts/validate_yaml.sh` | `scripts/validate_yaml.sh` | 変換不要（決定論的コード） |

### 第3層（手順保証層）

| Claude Code | Codex CLI | 差異 |
|-------------|-----------|------|
| `.claude/settings.json` Stop hook | `codex.json` agent-stop | Codexの Stop は experimental（v0.114.0） |
| Stop hook: 失敗時にブロック | agent-stop: 失敗の報告のみ | ブロック強制力が異なる |
| PreToolUse hook | なし | Codexには実行前ブロック機構がない |

## 観察ポイント

1. **SKILL.md の解釈**: GPTモデルが同じSKILL.mdの手順をどの順序で実行するか
2. **Rules の遵守**: AGENTS.mdに統合した7種type・8種relationの制約が守られるか
3. **Hooks の強制力**: experimental Stop hookが validate_yaml.sh の結果に基づいて差し戻すか
4. **孤立ノード**: 第7章で段階3まで残り続けた `ribozyme_abundance` 相当の問題が、Hooks なしで解決されるか

## 実行方法

```bash
# 1. 入力PDFをコピー
cp ../../../chapter7/input/science.adt2760.pdf input/

# 2. スクリプトに実行権限を付与
chmod +x scripts/validate_yaml.sh

# 3. Codex CLI で実行
codex --model gpt-4.1 "AGENTS.mdを読み、.agents/skills/structurize/SKILL.mdに従って論文を構造化してください"
```
