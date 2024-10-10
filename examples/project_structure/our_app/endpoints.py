from fastapi import FastAPI, Request

from services.dummy_service import dummy_result

app = FastAPI()


@app.post("/v1/solver")
async def resolve(input: Request):
    """Solve the task.

    Args:
        input: Task input. Document?

    Returns: Task output.
    """
    return dummy_result()
