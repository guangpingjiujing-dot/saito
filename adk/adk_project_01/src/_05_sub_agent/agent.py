from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.google_search_tool import google_search


def add(a: int, b: int) -> int:
    """2つの整数の和を返す。足し算が必要なときに使う。"""
    return a + b


# サブエージェント1: _02 と同様に Google 検索だけを担当
# Gemini API はビルトインの google_search と Function Calling（例: transfer_to_agent）を
# 同一リクエストに載せられない。サブエージェントは通常ピアや親への転送ツールが付くため、
# 検索担当だけ転送を切り、リクエストは google_search のみにする。
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

# サブエージェント2: _03 の function tool のみを担当（複数ツール制限を避けるため検索は付けない）
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

# 親エージェント: サブへは transfer_to_agent（ADK が自動でツールと説明を付与）
root_agent = Agent(
    name="sub_agent_coordinator",
    model="gemini-2.5-flash",
    description=(
        "ユーザーの窓口。雑談や一般的な説明はここで返す。"
        "検索や正確な加算が主題のときは、説明に従って適切なサブエージェントに任せる。"
    ),
    instruction=(
        "あなたは親エージェント（コーディネーター）。"
        "フレームワークが追加するエージェント間転送の説明に従い、"
        "自分が一番ふさわしいと思うところで答え、専門サブのほうが適しているときは転送する。"
    ),
    sub_agents=[search_specialist, math_specialist],
)
