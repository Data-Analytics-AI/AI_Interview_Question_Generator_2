'''# app/prompt_templates.py
from typing import List
import json

BASE_PROMPT_INSTRUCTIONS = """
You are an expert technical interviewer. Given a job description and generation settings, output a JSON object strictly matching the "OUTPUT_SCHEMA" below.
You must produce high-quality interview questions that test skills, background, and behavioral fitness. Include follow-up questions if requested.
The generated output should be concise but complete and in valid JSON.
"""

OUTPUT_SCHEMA = {
    "job_title": "string or null",
    "extracted_key_skills": ["list", "of", "strings"],
    "seniority_level": "Junior | Mid | Senior | Unknown",
    "interview_duration_minutes": "integer or null",
    "questions": [
        {
            "id": "int",
            "category": "one of categories requested",
            "question": "string",
            "context": "optional scenario or context",
            "what_we_are_testing": ["list of strings"],
            "strong_answer_should_include": ["list of strings"],
            "red_flags": ["list of strings"],
            "follow_ups": ["list of strings"]
        }
    ],
    "interviewer_guide": "string"
}

def build_generation_prompt(
    job_title: str,
    job_description: str,
    categories: List[str],
    number_of_questions: int,
    difficulty: str,
    industry: str = None,
    include_followups: bool = True,
    followups_per_question: int = 1,
    interview_duration: int = None,
    reference_doc_path: str = None
) -> str:
    """
    Construct a careful prompt to instruct the model to emit structured JSON.
    """
    categories_str = ", ".join(categories)
    ref_text = f"\n\nReference format rules from the client's specification (file at: {reference_doc_path})." if reference_doc_path else ""
    prompt = BASE_PROMPT_INSTRUCTIONS + "\n\n"
    prompt += "OUTPUT_SCHEMA = " + json.dumps(OUTPUT_SCHEMA, indent=2) + "\n\n"
    prompt += f"JOB_TITLE: {job_title}\n\n" if job_title else ""
    prompt += "JOB_DESCRIPTION:\n" + job_description.strip() + "\n\n"
    prompt += f"CATEGORIES: {categories_str}\n"
    prompt += f"NUMBER_OF_QUESTIONS: {number_of_questions}\n"
    prompt += f"DIFFICULTY: {difficulty}\n"
    if industry:
        prompt += f"INDUSTRY: {industry}\n"
    prompt += f"INCLUDE_FOLLOWUPS: {'Yes' if include_followups else 'No'}\n"
    if include_followups:
        prompt += f"FOLLOWUPS_PER_QUESTION: {followups_per_question}\n"
    if interview_duration:
        prompt += f"INTERVIEW_DURATION_MINUTES: {interview_duration}\n"
    if reference_doc_path:
        prompt += ref_text + "\n\n"
    prompt += (
        "CONSTRAINTS:\n"
        "1) Output must be valid JSON that fits the OUTPUT_SCHEMA exactly.\n"
        "2) For each question include: context (if helpful), what_we_are_testing, strong_answer_should_include and red_flags.\n"
        "3) Distribute categories across questions roughly evenly; if difficulty is Mixed, auto-distribute easy/medium/hard.\n"
        "4) For extracted_key_skills invent a short list of the top technologies/skills mentioned in the JD.\n"
        "5) Keep each question's text under 250 words.\n\n"
        "Return only JSON.\n"
    )
    return prompt

# app/prompt_templates.py
from typing import List
import json

BASE_PROMPT_INSTRUCTIONS = """You are an expert interviewer. Given a Job Description and settings, produce a single VALID JSON object matching OUTPUT_SCHEMA exactly. Do not include any extra text."""

OUTPUT_SCHEMA = {
  "job_title": "string or null",
  "extracted_key_skills": ["list", "of", "strings"],
  "seniority_level": "Junior | Mid | Senior | Unknown",
  "interview_duration_minutes": "integer or null",
  "questions": [
    {
      "id": "int",
      "category": "one of categories requested",
      "question": "string",
      "context": "optional scenario or context",
      "what_we_are_testing": ["list of strings"],
      "strong_answer_should_include": ["list of strings"],
      "red_flags": ["list of strings"],
      "follow_ups": ["list of strings"]
    }
  ],
  "interviewer_guide": "string"
}

def build_generation_prompt(
    job_title: str,
    job_description: str,
    categories: List[str],
    number_of_questions: int,
    difficulty: str,
    industry: str | None = None,
    include_followups: bool = True,
    followups_per_question: int = 1,
    interview_duration: int | None = None,
    reference_doc_path: str | None = None,
) -> str:
    categories_str = ", ".join(categories)
    prompt = BASE_PROMPT_INSTRUCTIONS + "\n\n"
    prompt += "OUTPUT_SCHEMA = " + json.dumps(OUTPUT_SCHEMA, indent=2) + "\n\n"
    if job_title:
        prompt += f"JOB_TITLE: {job_title}\n\n"
    prompt += "JOB_DESCRIPTION:\n" + job_description.strip() + "\n\n"
    prompt += f"CATEGORIES: {categories_str}\n"
    prompt += f"NUMBER_OF_QUESTIONS: {number_of_questions}\n"
    prompt += f"DIFFICULTY: {difficulty}\n"
    if industry:
        prompt += f"INDUSTRY: {industry}\n"
    prompt += f"INCLUDE_FOLLOWUPS: {'Yes' if include_followups else 'No'}\n"
    if include_followups:
        prompt += f"FOLLOWUPS_PER_QUESTION: {followups_per_question}\n"
    if interview_duration:
        prompt += f"INTERVIEW_DURATION_MINUTES: {interview_duration}\n"
    if reference_doc_path:
        prompt += f"\nReference: follow rules from the file at {reference_doc_path}\n\n"
    prompt += (
        "CONSTRAINTS:\n"
        "1) Output must be valid JSON that fits the OUTPUT_SCHEMA exactly.\n"
        "2) For each question include: context (if helpful), what_we_are_testing, strong_answer_should_include and red_flags.\n"
        "3) Distribute categories across questions roughly evenly; if difficulty is Mixed, auto-distribute easy/medium/hard.\n"
        "4) For extracted_key_skills invent a short list of the top technologies/skills mentioned in the JD.\n"
        "5) Keep each question's text under 250 words.\n\n"
    )
    return prompt'''

# app/prompt_templates.py
import json
from typing import List

OUTPUT_SCHEMA = {
    "job_title": "string (infer it from the job description)",
    "extracted_key_skills": ["list of strings"],
    "seniority_level": "Junior | Mid | Senior | Unknown",
    "interview_duration_minutes": "integer",
    "questions": [
        {
            "id": "int",
            "category": "string",
            "question": "string",
            "context": "string",
            "what_we_are_testing": ["list"],
            "strong_answer_should_include": ["list"],
            "red_flags": ["list"],
            "follow_ups": ["list"]
        }
    ],
    "interviewer_guide": "string"
}


def build_generation_prompt(
    job_description: str,
    categories: List[str],
    number_of_questions: int,
    difficulty: str,
    industry: str,
    #industry_specific_scenarios: List[str],
    include_followups: bool,
    followups_per_question: int
):
    categories_str = ", ".join(categories)
    #scenario_str = "\n".join(f"- {s}" for s in industry_specific_scenarios) if industry_specific_scenarios else "None provided"

    prompt = f"""
You are an advanced interviewer AI. Generate structured interview questions in JSON using the OUTPUT_SCHEMA below:

OUTPUT_SCHEMA:
{json.dumps(OUTPUT_SCHEMA, indent=2)}

GUIDELINES:
- Infer the job title directly from the job description.
- Produce questions that assess technical depth, behavioral traits, communication, and problem-solving.
- Use the industry-specific scenarios when they exist.
- Distribute categories evenly across the generated questions.
- Difficulty: {difficulty}.
- If follow-ups are included, generate {followups_per_question} per question.
- Infer a realistic interview duration based on the number of questions and complexity.
- Return ONLY JSON. No explanations.

JOB_DESCRIPTION:
{job_description}

CATEGORIES REQUESTED: {categories_str}
NUMBER_OF_QUESTIONS: {number_of_questions}
INDUSTRY: {industry or "Not specified"}



INCLUDE_FOLLOWUPS: {include_followups}
FOLLOWUPS_PER_QUESTION: {followups_per_question}

Return ONLY valid JSON that fits OUTPUT_SCHEMA exactly.
"""
    return prompt
