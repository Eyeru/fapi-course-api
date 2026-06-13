from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
from app.core.logger import logger

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are allowed."
            )
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # Limit file size to 10MB
        raise HTTPException(
            status_code=400, 
            detail="File size exceeds the 10MB limit."
            )
    await file.seek(0)  # Reset file pointer after reading
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(f"File uploaded: {file.filename}")

    return {
        "filename": file.filename,
        "saved_to": file_path
    }
