# _10_a2a_minimal_agent

`RemoteA2aAgent` を使った最小サンプルです。  
親エージェントがリモートA2Aエージェントに処理を委譲します。

## 使い方

1. 依存を同期

```bash
uv sync
```

2. time_agent サーバーを起動（ターミナル1）

```bash
uv run src/_10_a2a_minimal_agent/time_agent_server.py
```

3. 接続先 Agent Card URL を設定（ターミナル2）

```bash
# PowerShell
$env:A2A_AGENT_CARD_URL="http://localhost:10001"
```

4. ADK Web を起動

```bash
adk web src/_10_a2a_minimal_agent
```

5. 質問例

```text
今何時？
```
