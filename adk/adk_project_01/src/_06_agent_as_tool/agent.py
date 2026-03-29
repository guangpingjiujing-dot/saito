from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search


def add(a: int, b: int) -> int:
    """2つの整数の和を返す。足し算が必要なときに使う。"""
    return a + b


# ツールとして呼び出すサブエージェント（中身は _05 と同じ役割分担）
# AgentTool 経由なら、親リクエストに transfer_to_agent は載らない。
# 検索担当はリクエストを google_search のみにできるよう、転送を切る。
search_specialist = Agent(
    name="search_specialist",
    model="gemini-2.5-flash",
    description=(
        "今日の天気、ニュース、製品の最新仕様など、Web で調べないと確かめづらい内容。"
        "ユーザーが「調べて」「最新は」など事実・時事の確認を求めているとき向け。"
    ),
    instruction=(
        "あなたは検索専門。回答にあたって必要なら google_search を使う。"
        "検索の必要がない話題なら、無理に検索せず短くその旨だけ答えてよい。"
    ),
    tools=[google_search],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

math_specialist = Agent(
    name="math_specialist",
    model="gemini-2.5-flash",
    description=(
        "2つの整数の足し算をツールで正確に計算することだけが役目。"
        "ユーザーが具体的な2整数の加算を依頼しているとき向け。"
    ),
    instruction="整数の和を求めるときは必ず add ツールを呼び出す。説明だけで答えを推測しない。",
    tools=[FunctionTool(add)],
)

# agent as tool: サブエージェントを transfer ではなく「1回のツール実行」として呼ぶ
root_agent = Agent(
    name="agent_as_tool_coordinator",
    model="gemini-2.5-flash",
    description=(
        "ユーザーの窓口。雑談や一般的な説明はここでそのまま返す。"
        "Web 調査が必要なら search_specialist を、正確な2整数の加算なら math_specialist を使う。"
    ),
    instruction=(
        "あなたは親エージェント。サブは sub_agents ではなくツールとして繋がっている。"
        "ツール名は search_specialist と math_specialist。"
        "検索や算術が主題なら、自分で答えず該当ツールに依頼し、返ってきた内容を要約してユーザーに伝える。"
        "ツールに渡す指示は、ユーザーが知りたいことをそのまま具体的に書く。"
    ),
    tools=[
        AgentTool(search_specialist),
        AgentTool(math_specialist),
    ],
)
