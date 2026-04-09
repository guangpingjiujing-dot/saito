import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

# ※サーバー側のツール名変更があれば、ここを書き換えてください。
_TOOL_FILTER = [
    "list_tables",
    "execute_sql",
    "get_advisors",
]


def _build_mcp_url() -> str:
    """Supabase MCP の URL を環境変数から組み立てる。"""
    project_ref = os.getenv("SUPABASE_PROJECT_REF")
    if not project_ref:
        raise RuntimeError(
            "Supabase project_ref が未設定です。.env に SUPABASE_PROJECT_REF を設定してください。"
        )
    return f"https://mcp.supabase.com/mcp?project_ref={project_ref}"


def _build_headers() -> dict[str, str]:
    """Supabase MCP 用の認証ヘッダーを組み立てる。"""
    token = os.getenv("SUPABASE_MCP_ACCESS_TOKEN") or os.getenv("SUPABASE_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(
            "Supabase MCP token が未設定です。.env に "
            "SUPABASE_MCP_ACCESS_TOKEN（または SUPABASE_ACCESS_TOKEN）を設定してください。"
        )
    return {"Authorization": f"Bearer {token}"}


supabase_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=_build_mcp_url(),
        headers=_build_headers(),
    ),
    tool_filter=_TOOL_FILTER,
)

root_agent = Agent(
    name="mcp_supabase_agent",
    model="gemini-2.5-flash",
    description="Supabase MCP に接続して DB 情報を調べるエージェント",
    instruction=(
        "あなたは Supabase の調査補助エージェントです。"
        "テーブル一覧、SQL 実行、アドバイザー確認が必要なときは MCP ツールを使ってください。"
        "不要なツール呼び出しは避け、結果は学習者に分かりやすく短く説明してください。"
    ),
    tools=[supabase_tools],
)
