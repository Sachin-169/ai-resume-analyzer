from flask import Blueprint, request
import os
from services.pdf_extractor import extract_text_from_pdf
from services.nlp_processor import process_text
from services.skill_extractor import extract_skills

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files: # Check if a file was uploaded
        return {
            "error": "No resume file uploaded."
        }, 400

    resume = request.files["resume"] # Get the uploaded file

    if resume.filename == "": # Check if the user actually selected a file
        return {
            "error": "No file selected."
        }, 400

    upload_folder = "uploads" # Create uploads folder if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, resume.filename)
    resume.save(file_path)

    resume_text = extract_text_from_pdf(file_path)
    doc = process_text(resume_text)
    skills = extract_skills(resume_text) # NEW: pull out known skills from the resume text

    return {
        "message": "Resume uploaded successfully!",
        "filename": resume.filename,
        "saved_to": file_path,
        "text": resume_text,
        "token_count": len(doc),
        "skills": skills # NEW
    }, 200