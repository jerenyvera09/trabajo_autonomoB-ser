from fastapi import APIRouter, UploadFile, File, HTTPException
import io
from PyPDF2 import PdfReader

router = APIRouter(prefix="/api/v1", tags=["pdf"])

@router.post("/pdf/extract")
async def extract_text_from_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    try:
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents))
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar PDF: {str(e)}")
