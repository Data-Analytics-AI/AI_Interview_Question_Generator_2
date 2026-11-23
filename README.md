# Recruitment AI Interview Questions Generator

Generates structured interview question packages from a Job Description using Azure OpenAI and serves via FastAPI.

**Reference input/output format used:** `/mnt/data/Recruitment AI generator input.pdf`. :contentReference[oaicite:1]{index=1}

## Features
- Accepts job description + generation settings (categories, number, difficulty, follow-ups).
- Produces structured JSON including questions, what they test, strong answers, red flags, follow-ups, and an interviewer guide.
- Deployable locally or via Docker.

## Files
- `app/` - application code
- `Dockerfile` - container image build
- `.env.example` - example environment variables
- `requirements.txt` - Python dependencies

## Setup (local, VSCode)
1. Clone project and open in VSCode.
2. Create `.env` (copy `.env.example`) and set:
   - `AZURE_OPENAI_ENDPOINT` e.g. `https://<your-resource>.openai.azure.com/`
   - `AZURE_OPENAI_KEY`
   - `AZURE_OPENAI_DEPLOYMENT` (the name of the deployment you set up in Azure)
   - `AZURE_OPENAI_API_VERSION` (optional)
3. (Optional) Install Python dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
