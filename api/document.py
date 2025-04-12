from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil, os, json, re
from rag.rag_utils import extract_term_definitions_from_pdf
from openai import OpenAI
from core.config import OPENAI_API_KEY

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/upload-dict/pdf")
async def extract_terms_from_pdf(file: UploadFile = File(...)):
    file_path = f"./temp_{file.filename}"
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        terms = extract_term_definitions_from_pdf(file_path)
        os.remove(file_path)
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": TERM_EXTRACTION_PROMPT + terms}],
                temperature=0.3,
        )
        content = response.choices[0].message.content.strip()

        json_start = content.find("[")
        if json_start != -1:
            content = content[json_start:]

        parsed = json.loads(content)
        return parsed
    except Exception as e:
        print(f"GPT 추출 실패: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract keywords.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

TERM_EXTRACTION_PROMPT = """
You are an expert assistant who extracts key technical terms and their definitions from a block of text.

Instructions:
1. Identify and extract important technical terms (1~2 words max) **that appear directly in the text**.
2. For each term, provide a short explanation based on the text or general knowledge.
3. Your response must be a **valid JSON array** only. Do not include any markdown, preamble, explanation, or formatting outside the JSON.
4. You must extract all IT-related technical terms present in the text and include each of them in the keyword field, with a corresponding simple description explaining the term.

Example Output:
[
  {"keyword": "Lambda", "description": "An anonymous function in Python used for short operations."},
  {"keyword": "Callback", "description": "A function passed into another function to be executed later."}
]

Text:
{text}

Return only the JSON list.
"""


@router.post("/upload-dict/text")
async def extract_term_definitions_from_text(text: str) -> list[dict]:
    prompt = TERM_EXTRACTION_PROMPT + text + "\nReturn only a valid JSON list as shown above. Do not add extra explanations or markdown formatting."


    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content.strip()

        # JSON 시작 부분 추출 (혹시 앞에 이상한 문장이 붙었을 경우 대비)
        json_start = content.find("[")
        if json_start != -1:
            content = content[json_start:]

        parsed = json.loads(content)
        return parsed
    except Exception as e:
        print(f"GPT 추출 실패: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract keywords.")