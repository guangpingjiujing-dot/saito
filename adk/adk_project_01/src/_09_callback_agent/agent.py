from typing import Any

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext


def greet(tool_context: ToolContext, name: str | None = None) -> str:
    """state を優先して名前付き挨拶を返すツール。"""
    final_name = name or tool_context.state.get("student_name")
    return f"{final_name}さん、こんにちは。"


def before_agent_callback(callback_context: CallbackContext):
    """エージェント実行前に呼ばれる最小コールバック。"""
    if "student_name" not in callback_context.state:
        callback_context.state["student_name"] = "学習者"
    return None


def before_tool_callback(tool: Any, args: dict[str, Any], tool_context: ToolContext):
    """ツール実行前に引数を補完する最小コールバック。"""
    if tool.name != "greet":
        return None

    if not args.get("name"):
        args["name"] = tool_context.state.get("student_name", "学習者")
    return None


root_agent = Agent(
    name="callback_agent",
    model="gemini-2.5-flash",
    description="コールバックの最小例（before_agent_callback / before_tool_callback）",
    instruction=(
        "ユーザーの質問に簡潔に回答してください。"
        "可能ならセッション変数 student_name を使って、やさしい語調で呼びかけてください。"
        "挨拶を求められたときは greet ツールを使ってください。"
    ),
    before_agent_callback=before_agent_callback,
    before_tool_callback=before_tool_callback,
    tools=[FunctionTool(greet)],
)
