'''# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    job_title: Optional[str] = None
    job_description: str
    categories: Optional[List[str]] = ["Technical/Coding", "Behavioral/Situational"]
    number_of_questions: int = 10
    difficulty: str = "Mixed"  # Easy, Medium, Hard, Mixed
    industry: Optional[str] = None
    include_followups: bool = True
    followups_per_question: int = 1
    interview_duration_minutes: Optional[int] = None

class QuestionOutput(BaseModel):
    id: int
    category: str
    question: str
    context: Optional[str] = None
    what_we_are_testing: Optional[List[str]] = None
    strong_answer_should_include: Optional[List[str]] = None
    red_flags: Optional[List[str]] = None
    follow_ups: Optional[List[str]] = None

class GenerateResponse(BaseModel):
    job_title: Optional[str]
    extracted_key_skills: List[str]
    seniority_level: Optional[str]
    interview_duration_minutes: Optional[int]
    questions: List[QuestionOutput]
    interviewer_guide: Optional[str]'''

# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    job_description: str
    categories: Optional[List[str]] = ["Technical", "Behavioral", "Problem-Solving"]
    number_of_questions: int = 10
    difficulty: str = "Mixed"
    industry: Optional[str] = None
    #industry_specific_scenarios: Optional[List[str]] = []
    include_followups: bool = True
    followups_per_question: int = 1


class QuestionOutput(BaseModel):
    id: int
    category: str
    question: str
    context: Optional[str]
    what_we_are_testing: Optional[List[str]]
    strong_answer_should_include: Optional[List[str]]
    red_flags: Optional[List[str]]
    follow_ups: Optional[List[str]]


class GenerateResponse(BaseModel):
    job_title: str
    extracted_key_skills: List[str]
    seniority_level: Optional[str]
    interview_duration_minutes: int
    questions: List[QuestionOutput]
    interviewer_guide: Optional[str]
