import os,uuid
from typing import Annotated

from fastapi import UploadFile, File,Depends
from sqlalchemy.exc import IntegrityError
from models import Statement
from database import get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload_file(
        file : UploadFile = File(...),
        db : Annotated = Depends(get_db)
):
    if file.content_type != "application/pdf":
        raise TypeError("Only PDF files allowed")
    
    unique_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        new_statement = Statement(
            filename=unique_name
        )
        db.add(new_statement)
        db.commit()
        db.refresh(new_statement)
    
    except Exception as e:
        db.rollback()
        raise ValueError(str(e)) from e
