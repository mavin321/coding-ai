# backend/routers/ai.py

from fastapi import APIRouter
from pydantic import BaseModel

from  backend.model_client import generate_response
from prompts import (
    make_explain_prompt,
    make_generate_prompt,
    make_refactor_prompt,
    make_tests_prompt
)

router = APIRouter(tags=["AI"])

class ExplainRequest(BaseModel):
    code: str
    language: str = "python"

class GenerateRequest(BaseModel):
    instruction: str
    language: str = "python"

class RefactorRequest(BaseModel):
    code: str
    language: str = "python"

class TestGenRequest(BaseModel):
    code: str
    function_name: str
    language: str = "python"


@router.post("/explain")
def explain_code(req: ExplainRequest):
    prompt = make_explain_prompt(req.code, req.language)
    output = generate_response(prompt)
    return {"response": output}


@router.post("/generate")
def generate_code(req: GenerateRequest):
    prompt = make_generate_prompt(req.instruction, req.language)
    output = generate_response(prompt)
    return {"response": output}


@router.post("/refactor")
def refactor_code(req: RefactorRequest):
    prompt = make_refactor_prompt(req.code, req.language)
    output = generate_response(prompt)
    return {"response": output}


@router.post("/tests")
def generate_tests(req: TestGenRequest):
    prompt = make_tests_prompt(req.code, req.function_name, req.language)
    output = generate_response(prompt)
    return {"response": output}
