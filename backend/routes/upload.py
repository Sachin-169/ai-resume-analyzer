from flask import Blueprint, request
import os
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

    return {
        "message": "Resume uploaded successfully!",
        "filename": resume.filename,
        "saved_to": file_path
    }, 200