from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search

root_agent = Agent(
    name="built_in_tool_agent",
    model="gemini-2.5-flash",
    description="Google検索を使用して情報を取得するエージェント",
    instruction="ユーザーからの質問に対して必要に応じてGoogle検索を使用して情報を取得して簡単に回答してください",
    tools=[google_search],
)
