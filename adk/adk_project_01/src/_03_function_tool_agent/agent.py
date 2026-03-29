from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool

# adk_project_01/output（このリポジトリ直下）
_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"


def add(a: int, b: int) -> int:
    """2つの整数の和を返す。"""
    return a + b


def save_answer_to_file(filename: str, content: str) -> str:
    """回答などのテキストを output フォルダに UTF-8 で保存する。filename は .txt など拡張子付きが望ましい。"""
    safe_name = Path(filename).name
    if not safe_name:
        return "エラー: ファイル名が空です。"

    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = _OUTPUT_DIR / safe_name
    path.write_text(content, encoding="utf-8")
    return f"保存しました: {path}"


root_agent = Agent(
    name="function_tool_agent",
    model="gemini-2.5-flash",
    description="独自の Python 関数をツールとして使うエージェント",
    instruction=(
        "ユーザーの質問に答えてください。"
        "足し算が必要なときは add ツールを使ってください。"
        "ユーザーがファイルに保存してほしいと言ったとき、最終的な回答文を save_answer_to_file で output に書き出してください。"
        "（保存しろと明示がなくても、保存を依頼されたら同様に使ってよいです）"
    ),
    tools=[FunctionTool(add), FunctionTool(save_answer_to_file)],
)
