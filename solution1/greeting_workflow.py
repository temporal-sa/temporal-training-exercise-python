from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from greeting_activity import create_greeting


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def greet(self, name: str) -> str:
        return await workflow.execute_activity(
            create_greeting,
            name,
            start_to_close_timeout=timedelta(seconds=5),
        )