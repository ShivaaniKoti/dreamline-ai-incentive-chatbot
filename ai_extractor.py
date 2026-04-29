import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return text

def extract_incentive_data(page_text, url):
    prompt = f"""
Extract structured incentive program data from this webpage text.

Return ONLY valid JSON.

Fields:
program_name, state, city, incentive_type, property_type,
description, eligibility_criteria, incentive_amount,
valid_until, updated_at, review_needed, program_links

Rules:
- If missing → null
- review_needed = "Yes" if unclear
- incentive_type must be: Grants, Rebates, Finance Solutions, Tax Credits, Investments
- program_links = {url}

TEXT:
{page_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Extract clean JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(clean_json_response(content))
