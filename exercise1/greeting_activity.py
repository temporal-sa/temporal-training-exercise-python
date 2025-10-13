from temporalio import activity


@activity.defn
async def create_greeting(name: str) -> str:
    # TODO: Return a greeting message in the format "Hello, [name]!"
    return None  # Replace with actual greeting