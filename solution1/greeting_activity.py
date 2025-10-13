from temporalio import activity


@activity.defn
async def create_greeting(name: str) -> str:
    return f"Hello, {name}!"