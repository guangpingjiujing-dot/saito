import datetime

import uvicorn
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard, AgentSkill, Part, TaskState, TextPart
from a2a.utils import new_agent_text_message, new_task


class TimeAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.current_task:
            task = context.current_task
        else:
            if context.message is None:
                raise ValueError("message is required")
            task = new_task(context.message)
        await event_queue.enqueue_event(task)

        context_id = getattr(task, "contextId", getattr(task, "context_id", task.id))
        updater = TaskUpdater(event_queue, task.id, context_id)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        text = f"現在時刻(UTC): {now}"

        await updater.update_status(
            TaskState.working,
            new_agent_text_message("時刻を取得しています...", context_id, task.id),
        )
        await updater.add_artifact(
            [Part(root=TextPart(text=text))],
            name="response",
        )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("cancel は未実装です。")


def main() -> None:
    skill = AgentSkill(
        id="tell_time",
        name="Tell Current Time",
        description="現在時刻(UTC)を返す",
        tags=["time"],
        examples=["今何時？"],
    )
    card = AgentCard(
        name="time_agent",
        description="現在時刻を返す最小A2Aエージェント",
        url="http://localhost:10001/",
        version="1.0.0",
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    app = A2AStarletteApplication(
        agent_card=card,
        http_handler=DefaultRequestHandler(
            agent_executor=TimeAgentExecutor(),
            task_store=InMemoryTaskStore(),
        ),
    )
    uvicorn.run(app.build(), host="127.0.0.1", port=10001)


if __name__ == "__main__":
    main()
