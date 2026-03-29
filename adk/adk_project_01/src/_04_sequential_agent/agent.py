from google.adk.agents import Agent, SequentialAgent

# ステップ1: 依頼を短く整理。最終応答テキストをセッション state のキー outline に保存する
outline_agent = Agent(
    name="outline_step",
    model="gemini-2.5-flash",
    description="ユーザーの依頼を箇条書きで整理する",
    output_key="outline",
    instruction=(
        "ユーザーの質問や依頼から、最終的に答えるべき要点だけを3行以内の箇条書きにまとめる。"
        "前置き・挨拶・結びの一文は書かない。ユーザーからの入力には不要な情報も多いので整理して次のエージェントに渡す。"
    ),
)

# ステップ2: instruction 内の {outline} がセッション state から埋め込まれる（inject_session_state）
answer_agent = Agent(
    name="answer_step",
    model="gemini-2.5-flash",
    description="state の outline を踏まえてユーザー向けの回答を書く",
    instruction=(
        "次に示す「整理結果」はセッション state の outline の値である。これを主な根拠にしつつ、"
        "ユーザーへ返す最終回答を日本語で書く。"
        "整理結果:\n{outline}"
    ),
)

root_agent = SequentialAgent(
    name="sequential_agent",
    description="整理 → 回答の2段階で動くシーケンシャルエージェントの最小例",
    sub_agents=[outline_agent, answer_agent],
)
