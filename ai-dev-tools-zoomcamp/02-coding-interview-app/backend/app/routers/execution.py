from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["execution"])

class ExecutionRequest(BaseModel):
    code: str
    language: str

class ExecutionResponse(BaseModel):
    output: str
    error: str | None = None

import subprocess
import tempfile
import os

@router.post("/execute", response_model=ExecutionResponse)
async def execute_code(request: ExecutionRequest):
    if request.language == "python":
        return execute_python(request.code)
    elif request.language == "javascript":
        return execute_javascript(request.code)
    else:
        return ExecutionResponse(output="Execution not supported for this language yet.", error="Unsupported Language")

def execute_python(code: str) -> ExecutionResponse:
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        
        # Run the code
        result = subprocess.run(
            ['python3', tmp_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Cleanup
        os.unlink(tmp_path)
        
        return ExecutionResponse(output=result.stdout + result.stderr)
    except Exception as e:
        return ExecutionResponse(output="", error=str(e))

def execute_javascript(code: str) -> ExecutionResponse:
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
            
        result = subprocess.run(
            ['node', tmp_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        os.unlink(tmp_path)
        
        return ExecutionResponse(output=result.stdout + result.stderr)
    except Exception as e:
        return ExecutionResponse(output="", error=str(e))
