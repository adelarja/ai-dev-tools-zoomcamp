from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["execution"])

class ExecutionRequest(BaseModel):
    code: str
    language: str

class ExecutionResponse(BaseModel):
    output: str
    error: str | None = None

@router.post("/execute", response_model=ExecutionResponse)
async def execute_code(request: ExecutionRequest):
    # Mock execution for now
    # In a real scenario, this would call Piston or a local runner
    return ExecutionResponse(output=f"Executed {request.language} code:\n{request.code}\n\n[Mock Output]", error=None)
