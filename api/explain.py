from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db import get_db
from crud.keyword import upsert_keyword
from models.explain import ExplainRequest, ExplainResponse, Explanation
from openai import OpenAI
from core.config import OPENAI_API_KEY
from models.extra_explain import ExtraExplainResponse, ExtraExplainRequest
from prompts.fewshot_prompt import get_explain_prompt
from prompts.fewshot_prompt import get_additional_explain_prompt
from utils.output_parser import format_explanation_to_text
from models.dict import Dict
import json

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/explain", response_model=ExplainResponse)
async def explain_text(request: ExplainRequest, db: Session = Depends(get_db)):
    text = request.text
    server_id = request.server_id
    platform = request.platform

    from models.server import Server
    server = db.query(Server).filter(
        Server.server_id == server_id,
        Server.platform == platform
    ).first()

    if not server:
        # 서버가 등록되지 않은 경우: 일반 프롬프트 사용
        prompt = get_explain_prompt(text)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            content = response.choices[0].message.content
            parsed = json.loads(content)

            keyword_entries = parsed.get("keywords", [])
            for entry in keyword_entries:
                if ":" in entry:
                    keyword_term = entry.split(":")[0].strip()
                    upsert_keyword(db, platform=platform, keyword=keyword_term)

            explanation_text = format_explanation_to_text(parsed)
            return ExplainResponse(result=explanation_text)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate explanation: {str(e)}"
            )

    else:
        # 서버가 등록된 경우: 해당 서버 사전 정보 포함
        dict_entries = db.query(Dict).filter(Dict.server_id == server.id).all()
        formatted_dict = "\n".join([f"{entry.keyword}: {entry.description}" for entry in dict_entries])

        # 프롬프트 생성
        prompt = get_explain_prompt(text) + f"\n\n[Please refer to it unconditionally]\n{formatted_dict}"

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            content = response.choices[0].message.content
            parsed = json.loads(content)

            # 🔍 서버 dict 키워드 목록 (소문자 기준으로 비교)
            dict_keywords = {entry.keyword.strip().lower() for entry in dict_entries}

            keyword_entries = parsed.get("keywords", [])
            updated_keywords = []

            for entry in keyword_entries:
                if ":" in entry:
                    keyword_term = entry.split(":")[0].strip()
                    description = entry.split(":")[1].strip()

                    # 서버 사전에 등록된 키워드 여부 판단
                    is_registered = keyword_term.lower() in dict_keywords

                    # 사용자에게 보여줄 용어명 가공
                    display_keyword = f"{keyword_term} (In Dict)" if is_registered else keyword_term

                    updated_keywords.append(f"{display_keyword}: {description}")

            # 업데이트된 키워드 반영
            parsed["keywords"] = updated_keywords

            # 설명 포맷 가공 후 응답
            explanation_text = format_explanation_to_text(parsed)
            return ExplainResponse(result=explanation_text)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate explanation: {str(e)}"
            )

@router.post("/explain-more", response_model=ExtraExplainResponse)
async def explain_more(request: ExtraExplainRequest, db: Session = Depends(get_db)):
    text = request.text
    server_id = request.server_id
    platform = request.platform

    from models.server import Server
    server = db.query(Server).filter(
        Server.server_id == server_id,
        Server.platform == platform
    ).first()

    dict_context = ""
    dict_keywords = set()

    if server:
        dict_entries = db.query(Dict).filter(Dict.server_id == server.id).all()
        dict_context = "\n\n[Please refer to it unconditionally]\n" + "\n".join(
            [f"{entry.keyword}: {entry.description}" for entry in dict_entries]
        )
        dict_keywords = {entry.keyword.strip().lower() for entry in dict_entries}

    # prompt 구성
    prompt = get_additional_explain_prompt(text, request.result) + dict_context

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)

        # 키워드에 (In Dict) 붙이기
        keyword_entries = parsed.get("keywords", [])
        updated_keywords = []

        for entry in keyword_entries:
            if ":" in entry:
                keyword_term = entry.split(":")[0].strip()
                description = entry.split(":")[1].strip()
                is_registered = keyword_term.lower() in dict_keywords
                display_keyword = f"{keyword_term} (In Dict)" if is_registered else keyword_term
                updated_keywords.append(f"{display_keyword}: {description}")

        parsed["keywords"] = updated_keywords

        explanation_text = format_explanation_to_text(parsed)
        return ExtraExplainResponse(result=explanation_text)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )
