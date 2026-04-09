import os

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent


a2a_card_url = os.getenv("A2A_AGENT_CARD_URL", "http://localhost:10001")

time_agent = RemoteA2aAgent(
    name="time_agent",
    description="現在時刻を返すリモートA2Aエージェント",
    agent_card=a2a_card_url,
)

root_agent = Agent(
    name="a2a_parent_agent",
    model="gemini-2.5-flash",
    description="RemoteA2aAgent を使う最小の親エージェント",
    instruction=(
        "ユーザーが時刻を聞いたら必ず time_agent に問い合わせてください。"
        "回答は短く、学習者にやさしい日本語で返してください。"
    ),
    sub_agents=[time_agent],
)
