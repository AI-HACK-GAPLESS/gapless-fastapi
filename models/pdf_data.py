from pydantic import BaseModel

class Base64PDFRequest(BaseModel):
    encoded_pdf: str  # base64 인코딩된 PDF 문자열