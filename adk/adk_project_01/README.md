# ADK 学習プロジェクト（adk-project-01）

[Agent Development Kit（ADK）](https://google.github.io/adk-docs/) を初めて触る方向けのサンプル集です。`src` 以下に、段階的にお題の違うエージェントが並んでいます。

この README だけで次のことができることを目指しています。

1. **このフォルダのプロジェクトを自分の PC で動かす**
2. **ゼロから新しい ADK プロジェクトをつくる**

---

## 事前準備

次のどちらもあるとスムーズです。

| もの | 備考 |
|------|------|
| **Python 3.12 以上** | ADK が要求するバージョンです（`pyproject.toml` の `requires-python` と同じ）。 |
| **uv** | 仮想環境と依存関係の管理に使います。未導入なら [uv のインストール](https://docs.astral.sh/uv/getting-started/installation/) を参照。 |

API キーは課題に応じて用意します。

- **Gemini（Google AI）**: [Google AI Studio](https://aistudio.google.com/apikey) で API キーを発行し、環境変数 `GOOGLE_API_KEY` に設定します。
- **OpenAI（`_99_gpt_agent` など）**: [OpenAI の API キー](https://platform.openai.com/api-keys) を発行し、`OPENAI_API_KEY` に設定します。

**API キーは他人に見せたり、Git にコミットしたりしないでください。** このリポジトリの `.gitignore` では `.env` を除外しています。

---

## このプロジェクトのセットアップ

### 1. フォルダに移動

ターミナルで、この README があるディレクトリ（`adk_project_01`）に移動します。

### 2. 依存関係のインストール

```powershell
uv sync
```

`google-adk` などが仮想環境に入ります。

### 3. 環境変数（`.env`）

プロジェクトの**ルート**（`pyproject.toml` と並ぶ場所）に `.env` を置き、必要なキーを書きます。

例（実際の値は自分のキーに差し替えてください）。

```env
GOOGLE_API_KEY=（Google AI Studio で発行したキー）
OPENAI_API_KEY=（OpenAI 用の課題だけ必要なら）
```

ファイル名は `.env` のままにします（先頭のドットを忘れない）。

### 4. Web UI でエージェントを試す

プロジェクトルートで次を実行します。

```powershell
uv run adk web src
```

- `src` は「エージェントが並んでいるディレクトリ」です。
- ブラウザで表示された URL（既定では `http://127.0.0.1:8000` 付近）を開き、一覧からエージェントを選んで会話できます。
- 終了するときはターミナルで `Ctrl+C` です。

### 5. うまく動かないとき

- **`GOOGLE_API_KEY` が無い／間違っている**  
  Gemini を使うサンプルは Google のキーが必要です。
- **`OPENAI_API_KEY` が無い**  
  `_99_gpt_agent` のように OpenAI 経由のモデルを指定しているものだけ必要です。
- **Python のバージョン**  
  3.12 未満だとインストールや実行で失敗することがあります。`python --version` で確認してください。
- **公式の説明**  
  環境や認証の詳細は [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/) が一次情報です。

---

## フォルダ構成（`src` 以下）

`adk web` に渡すディレクトリでは、**1 つのサブフォルダ = 1 つのエージェント** という単位になります。各フォルダに `agent.py` があり、その中で `root_agent` を定義します。

| フォルダ | おおよその内容 |
|----------|----------------|
| `_01_first_agent` | 最小構成のエージェント（Gemini） |
| `_02_built_in_tool_agent` | 組み込みツールを使う例 |
| `_03_function_tool_agent` | 自分で定義した関数をツールにする例 |
| `_04_sequential_agent` | 複数ステップを順に進める例 |
| `_05_sub_agent` | サブエージェントの例 |
| `_06_agent_as_tool` | エージェントをツールとして呼ぶ例 |
| `_99_gpt_agent` | LiteLLM 経由で OpenAI を使う例 |


---

