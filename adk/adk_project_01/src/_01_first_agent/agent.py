from google.adk.agents import Agent

root_agent = Agent(
    name="first_agent",
    model="gemini-2.5-flash",
    description="もっとも基本的なエージェント",
    instruction="ユーザーからの質問に対して、簡単な回答を返す",
)