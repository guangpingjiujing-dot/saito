from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    name="gpt_agent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    description="OpenAI GPT を使う基本的なエージェント（LiteLLM 経由）",
    instruction="ユーザーからの質問に対して、簡単な回答を返す",
)
