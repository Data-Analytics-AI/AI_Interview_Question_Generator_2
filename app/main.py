'''# app/main.py
from fastapi import FastAPI, HTTPException
from .schemas import GenerateRequest, GenerateResponse, QuestionOutput
from .prompt_templates import build_generation_prompt
from .openai_client import generate_completion
from .utils import extract_text_from_pdf, simple_skill_extraction
from .config import settings
from typing import List
import json

app = FastAPI(title="Recruitment AI Question Generator")

# path to uploaded reference PDF (you provided this file)
REFERENCE_PDF_PATH = "/mnt/data/Recruitment AI generator input.pdf"

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        ref_text = extract_text_from_pdf(REFERENCE_PDF_PATH)
    except Exception:
        ref_text = ""  # non-fatal

    prompt = build_generation_prompt(
        job_title=req.job_title or "",
        job_description=req.job_description,
        categories=req.categories,
        number_of_questions=req.number_of_questions,
        difficulty=req.difficulty,
        industry=req.industry,
        include_followups=req.include_followups,
        followups_per_question=req.followups_per_question,
        interview_duration=req.interview_duration_minutes,
        reference_doc_path=REFERENCE_PDF_PATH
    )

    raw = generate_completion(prompt, temperature=0.0, max_tokens=1400)

    # Attempt to parse JSON from response; allow for trailing text
    try:
        # If model prints explanation + JSON, extract first {...}
        start = raw.find("{")
        end = raw.rfind("}")
        json_text = raw[start:end+1]
        data = json.loads(json_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse model response: {str(e)}. Raw output: {raw[:500]}")

    # Ensure fields exist and massage into response model
    questions = []
    for q in data.get("questions", []):
        questions.append(QuestionOutput(
            id=q.get("id"),
            category=q.get("category"),
            question=q.get("question"),
            context=q.get("context"),
            what_we_are_testing=q.get("what_we_are_testing"),
            strong_answer_should_include=q.get("strong_answer_should_include"),
            red_flags=q.get("red_flags"),
            follow_ups=q.get("follow_ups") or []
        ))

    resp = GenerateResponse(
        job_title=data.get("job_title") or req.job_title,
        extracted_key_skills=data.get("extracted_key_skills") or simple_skill_extraction(req.job_description),
        seniority_level=data.get("seniority_level") or "Unknown",
        interview_duration_minutes=data.get("interview_duration_minutes") or req.interview_duration_minutes,
        questions=questions,
        interviewer_guide=data.get("interviewer_guide")
    )
    return resp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)

# app/main.py
from fastapi import FastAPI, HTTPException
from .schemas import GenerateRequest, GenerateResponse, QuestionOutput
from .prompt_templates import build_generation_prompt
from .openai_client import generate_completion
from .utils import extract_text_from_pdf, simple_skill_extraction
from .config import settings
from typing import List
import json
import asyncio

app = FastAPI(title="Recruitment AI Question Generator (async, Pydantic v2)")

REFERENCE_PDF_PATH = "/mnt/data/Recruitment AI generator input.pdf"

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    # read reference PDF (sync IO; it's small and only used to enrich the prompt)
    ref_text = extract_text_from_pdf(REFERENCE_PDF_PATH)

    prompt = build_generation_prompt(
        job_title=req.job_title or "",
        job_description=req.job_description,
        categories=req.categories,
        number_of_questions=req.number_of_questions,
        difficulty=req.difficulty,
        industry=req.industry,
        include_followups=req.include_followups,
        followups_per_question=req.followups_per_question,
        interview_duration=req.interview_duration_minutes,
        reference_doc_path=REFERENCE_PDF_PATH
    )

    raw = await generate_completion(prompt, temperature=0.0, max_tokens=1400, deployment=settings.azure_openai_deployment)

    # Attempt to extract JSON object from model output
    try:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in model output.")
        json_text = raw[start:end+1]
        data = json.loads(json_text)
    except Exception as e:
        # return helpful error to caller (raw truncated)
        raise HTTPException(status_code=500, detail=f"Failed to parse model JSON. Error: {e}. Partial model output: {raw[:500]}")

    # Build questions list
    questions_list: List[QuestionOutput] = []
    for q in data.get("questions", []):
        questions_list.append(QuestionOutput(
            id=q.get("id"),
            category=q.get("category"),
            question=q.get("question"),
            context=q.get("context"),
            what_we_are_testing=q.get("what_we_are_testing"),
            strong_answer_should_include=q.get("strong_answer_should_include"),
            red_flags=q.get("red_flags"),
            follow_ups=q.get("follow_ups") or []
        ))

    resp = GenerateResponse(
        job_title=data.get("job_title") or req.job_title,
        extracted_key_skills=data.get("extracted_key_skills") or simple_skill_extraction(req.job_description),
        seniority_level=data.get("seniority_level") or "Unknown",
        interview_duration_minutes=data.get("interview_duration_minutes") or req.interview_duration_minutes,
        questions=questions_list,
        interviewer_guide=data.get("interviewer_guide")
    )
    return resp

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)'''

# app/main.py
from fastapi import FastAPI, HTTPException
import json

from .schemas import GenerateRequest, GenerateResponse, QuestionOutput
from .prompt_templates import build_generation_prompt
from .openai_client import generate_completion
from .utils import simple_skill_extraction
from .config import settings

app = FastAPI(title="AI Interview Questions Generator")


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):

    prompt = build_generation_prompt(
        #job_title=req.job_title or "Unknown role",
        job_description=req.job_description,
        categories=req.categories,
        number_of_questions=req.number_of_questions,
        difficulty=req.difficulty,
        industry=req.industry,
        include_followups=req.include_followups,
        followups_per_question=req.followups_per_question,
    )

    raw = generate_completion(prompt, temperature=0.0, max_tokens=3500)
    print(f"Model raw output: {raw}")  # log first 500 chars

    try:
        start = raw.find("{")
        end = raw.rfind("}")
        parsed = json.loads(raw[start:end+1])
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Model returned invalid JSON. Raw: {raw[:500]}"
        )

    questions = [
        QuestionOutput(
            id=q["id"],
            category=q["category"],
            question=q["question"],
            context=q.get("context"),
            what_we_are_testing=q.get("what_we_are_testing"),
            strong_answer_should_include=q.get("strong_answer_should_include"),
            red_flags=q.get("red_flags"),
            follow_ups=q.get("follow_ups", [])
        )
        for q in parsed.get("questions", [])
    ]

    return GenerateResponse(
        job_title=parsed.get("job_title", "Unknown"),
        extracted_key_skills=parsed.get("extracted_key_skills") or simple_skill_extraction(req.job_description),
        seniority_level=parsed.get("seniority_level", "Unknown"),
        interview_duration_minutes=parsed.get("interview_duration_minutes", 45),
        questions=questions,
        interviewer_guide=parsed.get("interviewer_guide", "")
    )


