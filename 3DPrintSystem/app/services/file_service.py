import os
import re
import json
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime, timezone

ALLOWED_EXTENSIONS = {'.stl', '.obj', '.3mf'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

def _get_last_id_file_path():
    """Get the path to last_file_id.txt, creating the directory if needed"""
    # Try to use workspace root relative to this file
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.join(current_file_dir, '..', '..', '..')
    workspace_root = os.path.normpath(workspace_root)
    
    cursor_dir = os.path.join(workspace_root, '.cursor')
    
    # Create .cursor directory if it doesn't exist
    if not os.path.exists(cursor_dir):
        os.makedirs(cursor_dir, exist_ok=True)
    
    return os.path.join(cursor_dir, 'last_file_id.txt')

def _get_next_id():
    last_id_file = _get_last_id_file_path()
    
    try:
        with open(last_id_file, 'r+') as f:
            last_id = f.read().strip()
            if not re.match(r'^[A-Z][0-9]+$', last_id) or last_id == "Z99": # Basic validation
                current_char_code = ord('A')
                current_num = 0
            else:
                current_char_code = ord(last_id[0])
                current_num = int(last_id[1:])

            current_num += 1
            if current_num > 99:
                current_num = 1
                current_char_code += 1
                if current_char_code > ord('Z'):
                    current_char_code = ord('A')
                    current_num = 1
            
            next_id_str = chr(current_char_code) + str(current_num)
            f.seek(0)
            f.write(next_id_str)
            f.truncate()
            return next_id_str
    except FileNotFoundError:
        # Create the file with initial value
        with open(last_id_file, 'w') as f:
            f.write("A1")
            return "A1"
    except Exception as e:
        current_app.logger.error(f"Error generating next ID: {e}")
        return "ERR00"

def generate_standardized_filename(student_name, print_method, color, job_id, original_filename):
    """Generate standardized filename for job files according to masterplan pattern"""
    # Clean student name (remove special characters and spaces)
    clean_name = re.sub(r'[^a-zA-Z\s]', '', student_name)
    clean_name = ''.join(clean_name.split())  # Remove spaces
    
    # Get file extension
    ext = os.path.splitext(original_filename)[1].lower()
    
    # Generate simple job ID (first 6 chars of UUID if job_id is UUID-like, otherwise use as-is)
    if len(job_id) > 6 and '-' in job_id:  # Looks like a UUID
        simple_id = job_id.replace('-', '')[:6].lower()
    else:
        simple_id = job_id.lower()
    
    # Follow masterplan pattern: FirstAndLastName_PrintMethod_Color_SimpleJobID.ext
    return f"{clean_name}_{print_method.capitalize()}_{color.replace('_', '').title()}_{simple_id}{ext}"

def is_allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file_storage):
    if not file_storage:
        return False, "No file selected."
    if file_storage.filename == '':
        return False, "No file selected."
    if not is_allowed_file(file_storage.filename):
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size (this requires reading the file, be careful with large files)
    # file_storage.seek(0, os.SEEK_END)
    # file_size = file_storage.tell()
    # file_storage.seek(0) # Reset cursor
    # if file_size > MAX_FILE_SIZE:
    #     return False, f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB."
    # A more robust way to check size without reading whole file into memory if possible with Flask/Werkzeug:
    # content_length is usually set by the client, can be spoofed.
    # For true size check before saving, one might need to stream it to a temp location or use a library.
    # For now, relying on client-side check and a basic server check if available.
    # Flask's request.content_length can give the size from header.
    
    return True, "File is valid."

def create_metadata_file(metadata_content, directory, filename_prefix):
    metadata_filename = f"{filename_prefix}.metadata.json"
    metadata_path = os.path.join(directory, metadata_filename)
    try:
        with open(metadata_path, 'w') as f:
            json.dump(metadata_content, f, indent=4)
        current_app.logger.info(f"Metadata file created: {metadata_path}")
        return metadata_path
    except Exception as e:
        current_app.logger.error(f"Could not create metadata file {metadata_path}: {e}")
        return None

def save_uploaded_file(file_storage, form_data):
    is_valid, message = validate_file(file_storage)
    if not is_valid:
        return None, message, None

    original_filename_secure = secure_filename(file_storage.filename)
    
    # Get form data for standardized naming
    student_name = form_data.get("studentName", "Unknown")
    print_method = form_data.get("printMethod", "Unknown")
    color = form_data.get("colorPreference", "Unknown")  # Frontend sends as 'colorPreference'
    
    # Generate a simple job ID for this submission
    job_id = _get_next_id()
    if job_id == "ERR00":
        return None, "Failed to generate a unique file ID. Please try again.", None

    # Use the standardized naming convention from masterplan
    new_model_filename = generate_standardized_filename(
        student_name=student_name,
        print_method=print_method,
        color=color,
        job_id=job_id,
        original_filename=original_filename_secure
    )
    
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'storage/Uploaded') 
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
        
    model_save_path = os.path.join(upload_folder, new_model_filename)
    
    try:
        file_storage.save(model_save_path)
        current_app.logger.info(f"File {original_filename_secure} saved as {new_model_filename} to {model_save_path}")
    except Exception as e:
        current_app.logger.error(f"Could not save file {new_model_filename}: {e}")
        return None, f"Could not save file: {e}", None

    # Create metadata content
    # The job_id field in metadata will initially be this file_id. 
    # It can be updated later when a database Job ID is available.
    metadata_content = {
        "temp_job_id": job_id, # Using file_id as a temporary job identifier
        "original_filename": file_storage.filename, # Non-secured, as submitted by user
        "display_name": new_model_filename, # The standardized filename
        "student_name": student_name,
        "student_email": form_data.get("studentEmail"),
        "discipline": form_data.get("discipline"),
        "class_number": form_data.get("classNumber"),
        "print_method": print_method,
        "color_preference": color,
        "printer_selection": form_data.get("printer"), # field name from submit.html
        "acknowledged_minimum_charge": form_data.get("minChargeConsent") == "yes",
        "submission_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "Uploaded",
        "notes_from_submission": form_data.get("notes") # Assuming 'notes' might be a field
    }

    # Use the standardized filename base for metadata file naming (without extension)
    filename_base = os.path.splitext(new_model_filename)[0]
    metadata_path = create_metadata_file(metadata_content, upload_folder, filename_base)
    if not metadata_path:
        # If metadata creation fails, what to do?
        # For now, log it and continue. The file is saved.
        # A more robust system might delete the saved model file or mark for review.
        current_app.logger.warning(f"Model file {new_model_filename} saved, but metadata creation failed.")
        # Return None for metadata_path to indicate failure
        return new_model_filename, model_save_path, None 
        
    return new_model_filename, model_save_path, metadata_path 