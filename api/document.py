from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil, os
from rag.rag_utils import extract_term_definitions_from_pdf

router = APIRouter()

@router.post("/upload-dict/pdf")
async def extract_terms_from_pdf(file: UploadFile = File(...)):
    file_path = f"./temp_{file.filename}"
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        terms = extract_term_definitions_from_pdf(file_path)
        os.remove(file_path)
        return {"terms": terms}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-dict/text")
async def extract_terms_from_text_file(file: UploadFile = File(...)):
    try:
        # 파일의 텍스트 내용 읽기
        content = await file.read()
        text = content.decode("utf-8")

        # 텍스트 기반 용어 정의 추출
        # TODO : extract_term_definitions_from_text 함수 구현 필요
        # terms = extract_term_definitions_from_text(text)
        # return {"terms": terms}
        return {"message": "Functionality not yet implemented."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))