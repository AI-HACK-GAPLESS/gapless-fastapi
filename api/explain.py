from fastapi import APIRouter, HTTPException
from models.explain import ExplainRequest, ExplainResponse, Explanation
from openai import OpenAI
from core.config import OPENAI_API_KEY
from prompts.fewshot_prompt import get_explain_prompt

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/explain", response_model=ExplainResponse)
async def explain_text(request: ExplainRequest):
    text = request.text

    prompt = get_explain_prompt(text)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        content = response.choices[0].message.content

        import json
        parsed = json.loads(content)

        def format_explanation_to_text(explanation: dict) -> str:
            summary = explanation["summary"]
            keywords = explanation["keywords"]

            keyword_lines = "\n".join(f"- {kw}" for kw in keywords)

            return f"Summary: {summary}\n\nKeywords:\n{keyword_lines}"
        
        explanation_text = format_explanation_to_text(parsed)
        return ExplainResponse(text=explanation_text)

        # return ExplainResponse(
        #     explanation=Explanation(
        #         term=text,
        #         summary=parsed.get("summary", ""),
        #         keywords=parsed.get("keywords", [])
        #     )
        # )
        # return ExplainResponse(
        #     explanation = format_explanation_to_text(parsed)
        # )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )