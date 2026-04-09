import asyncio
import datetime
import time

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.function_tool import FunctionTool


async def get_current_time() -> str:
    """現在時刻（ISO 形式）を返す。遅延を入れて並列実行の効果を観察しやすくしている。"""
    await asyncio.sleep(2)
    return datetime.datetime.now().isoformat()


async def get_weather(city: str, tool_context: ToolContext) -> dict:
    """都市の天気（ダミーデータ）を返す。遅延を入れて並列実行の効果を観察しやすくしている。"""
    await asyncio.sleep(2)

    weather_data = {
        "New York": {"temp": 72, "condition": "sunny", "humidity": 45},
        "London": {"temp": 60, "condition": "cloudy", "humidity": 80},
        "Tokyo": {"temp": 68, "condition": "rainy", "humidity": 90},
        "San Francisco": {"temp": 65, "condition": "foggy", "humidity": 85},
        "Paris": {"temp": 58, "condition": "overcast", "humidity": 70},
        "Sydney": {"temp": 75, "condition": "sunny", "humidity": 60},
    }

    result = weather_data.get(
        city,
        {
            "temp": 70,
            "condition": "unknown",
            "humidity": 50,
            "note": f"Weather data not available for {city}, showing default values",
        },
    )

    return {
        "city": city,
        "temperature": result["temp"],
        "condition": result["condition"],
        "humidity": result["humidity"],
        **({"note": result["note"]} if "note" in result else {}),
    }


root_agent = Agent(
    name="parallel_tool_agent",
    model="gemini-2.5-flash",
    description="複数ツールの同時（並列）実行を試すエージェント",
    instruction=(
        "ユーザーの質問に答えてください。"
        "天気に関する質問（特に複数都市）なら get_weather を使ってください。"
        "時間に関する質問なら get_current_time を使ってください。"
        "ユーザーが複数都市の天気や「天気と時間を両方」など複数のツール呼び出しを必要とする依頼をした場合、"
        "可能なら1回の応答でツール呼び出しをまとめ、同時に実行される形を狙ってください。"
    ),
    tools=[FunctionTool(get_weather), FunctionTool(get_current_time)],
)

