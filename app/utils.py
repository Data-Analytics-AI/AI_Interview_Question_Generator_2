# app/utils.py
import re
from typing import List

def simple_skill_extraction(job_description: str) -> List[str]:
    common = [
        "Python","Java","JavaScript","TypeScript","React","Node","SQL","Postgres",
        "AWS","Azure","GCP","Docker","Kubernetes","Redis","TensorFlow","PyTorch",
        "Machine Learning","Deep Learning"
    ]

    found = []
    lower = job_description.lower()

    for c in common:
        if c.lower() in lower and c not in found:
            found.append(c)

    # fallback: extract capitalized terms
    tokens = re.findall(r"\b[A-Z][a-zA-Z0-9\+\#\.]+\b", job_description)
    for t in tokens:
        if t not in found:
            found.append(t)

    return found[:10]
