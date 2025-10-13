from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from greeting_activity import create_greeting


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def greet(self, name: str) -> str:
        # TODO: Execute the create_greeting activity with:
        # - start_to_close_timeout of 5 seconds
        # - Pass the name parameter to the activity
        # - Return the result from the activity
        return None  # Replace with activity execution