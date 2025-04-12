from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil, os
from rag.rag_utils import extract_term_definitions_from_pdf

router = APIRouter()

@router.post("/upload-pdf")
async def extract_terms(file: UploadFile = File(...)):
    file_path = f"./temp_{file.filename}"
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        terms = extract_term_definitions_from_pdf(file_path)
        os.remove(file_path)
        return {"terms": terms}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))