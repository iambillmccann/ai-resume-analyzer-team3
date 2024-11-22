from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.dashboard import ResumeUploadResponse
from schemas.dashboard import JobDescriptionRequest
from utils.storage import store_data
from io import BytesIO
from docx import Document
import time

router = APIRouter()

@router.post("/resume-upload", response_model=ResumeUploadResponse)
async def upload_resume(resume_file: UploadFile = File(...)):
    # Allow both PDF and DOCX file types
    allowed_content_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    # Maximum file size = 2MB
    maximum_file_size_allowed = 1024 * 1024 * 2

    #Validate the file type
    if resume_file.content_type not in allowed_content_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are allowed.")
    #Validate the file size
    size_of_file = len(await resume_file.read())
    if maximum_file_size_allowed < size_of_file:
        raise HTTPException(status_code=400, detail="File cannot exceed 2MB. Check file size.")
    
    #Need to restart the file pointer since we read the file
    await resume_file.seek(0)
    
    # Read the file content
    content = await resume_file.read()
    
    # Process based on file type
    if resume_file.content_type == "application/pdf":
        # For PDFs, just store content directly (assuming PDF parsing occurs elsewhere if needed)
        text_content = content.decode('utf-8', errors="ignore")  # Handle binary content as needed for PDFs
    
    elif resume_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # For DOCX, use python-docx to read text
        doc = Document(BytesIO(content))
        text_content = "\n".join([para.text for para in doc.paragraphs])
    
    # Store the extracted text content in temporary storage
    store_data("resume", "temp_user", text_content)  # Replace "temp_user" with actual user identifier as needed

    # To test loading
    time.sleep(2)

    return {"message": "Resume uploaded successfully", "filename": resume_file.filename}

@router.post("/job-description")
async def handle_job_description(job_description: str = Form(...)):
    #Description should not exceed 5000 characters
    if len(job_description) > 5000:
        raise HTTPException(status_code=400, detail="Job description exceeds character limit.")
    
    #Clean the text by removing extraneous whitespace
    individual_words = job_description.split()
    clean_description = " ".join(individual_words)
    store_data("job_description", "temp_user", clean_description)  # Placeholder user ID for demo

    # To test loading
    time.sleep(2)

    return {"message": "Job description received successfully"}