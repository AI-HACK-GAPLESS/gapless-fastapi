from fastapi import APIRouter, HTTPException
from models.explain import ExplainRequest, ExplainResponse, Explanation
from openai import OpenAI
from core.config import OPENAI_API_KEY

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/explain", response_model=ExplainResponse)
async def explain_text(request: ExplainRequest):
    text = request.text

    prompt = f"""
    You are an expert assistant who helps users understand technical IT concepts in simple language.

    Given the following text, do the following two tasks:

    1. Extract a list of important technical keywords (focus on nouns or key terms).
    2. Summarize the overall meaning of the text in a way that a beginner can understand.

    Text: {text}

    Return your response in **valid JSON format** like below:

    {{
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "summary": "a simplified explanation of the whole text"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content

        import json
        parsed = json.loads(content)

        return ExplainResponse(
            explanation=Explanation(
                term=text,
                summary=parsed.get("summary", ""),
                keywords=parsed.get("keywords", [])
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )