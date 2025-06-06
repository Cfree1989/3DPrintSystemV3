from typing import Any, Dict, Optional, Tuple, Union
from flask import jsonify, request, flash, redirect, url_for
from werkzeug.exceptions import BadRequest
from .validation import ValidationError, validate_form_data, validate_json_data

class FormHandler:
    """Utility class for handling form submissions and errors"""
    
    @staticmethod
    def handle_form_submission(
        schema: Dict[str, list],
        success_url: str,
        error_url: Optional[str] = None,
        success_message: Optional[str] = None,
        process_data: Optional[callable] = None
    ) -> Union[Tuple[Dict[str, Any], int], redirect]:
        """
        Handle form submission with validation and error handling
        
        Args:
            schema: Validation schema for form data
            success_url: URL to redirect on success
            error_url: URL to redirect on error (defaults to current URL)
            success_message: Message to flash on success
            process_data: Optional callback to process validated data
            
        Returns:
            Tuple of (response, status_code) for AJAX requests
            or redirect response for regular form submissions
        """
        try:
            # Validate form data
            if request.is_xhr:
                data = validate_json_data(schema)
            else:
                data = validate_form_data(schema)
            
            # Process data if callback provided
            if process_data:
                result = process_data(data)
                if result:
                    data = result
            
            # Handle response
            if request.is_xhr:
                return jsonify({
                    'success': True,
                    'data': data,
                    'redirect': success_url
                })
            
            if success_message:
                flash(success_message, 'success')
            return redirect(url_for(success_url))
            
        except ValidationError as e:
            if request.is_xhr:
                return jsonify({
                    'success': False,
                    'errors': e.errors
                }), 400
            
            for field, message in e.errors.items():
                flash(f"{field}: {message}", 'error')
            return redirect(error_url or request.url)
            
        except Exception as e:
            if request.is_xhr:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
            
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(error_url or request.url)
    
    @staticmethod
    def handle_file_upload(
        file_field: str,
        allowed_types: list,
        max_size_mb: int,
        upload_dir: str,
        success_url: str,
        error_url: Optional[str] = None,
        success_message: Optional[str] = None,
        process_file: Optional[callable] = None
    ) -> Union[Tuple[Dict[str, Any], int], redirect]:
        """
        Handle file upload with validation and error handling
        
        Args:
            file_field: Name of the file input field
            allowed_types: List of allowed MIME types
            max_size_mb: Maximum file size in MB
            upload_dir: Directory to save uploaded files
            success_url: URL to redirect on success
            error_url: URL to redirect on error
            success_message: Message to flash on success
            process_file: Optional callback to process uploaded file
            
        Returns:
            Tuple of (response, status_code) for AJAX requests
            or redirect response for regular form submissions
        """
        try:
            if file_field not in request.files:
                raise ValidationError("No file uploaded")
            
            file = request.files[file_field]
            if not file.filename:
                raise ValidationError("No file selected")
            
            # Validate file
            if file.content_type not in allowed_types:
                raise ValidationError(f"File type must be one of: {', '.join(allowed_types)}")
            
            if file.content_length > max_size_mb * 1024 * 1024:
                raise ValidationError(f"File size must be less than {max_size_mb}MB")
            
            # Process file if callback provided
            if process_file:
                result = process_file(file)
                if result:
                    file = result
            
            # Save file
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Handle response
            if request.is_xhr:
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'redirect': success_url
                })
            
            if success_message:
                flash(success_message, 'success')
            return redirect(url_for(success_url))
            
        except ValidationError as e:
            if request.is_xhr:
                return jsonify({
                    'success': False,
                    'errors': e.errors
                }), 400
            
            flash(str(e), 'error')
            return redirect(error_url or request.url)
            
        except Exception as e:
            if request.is_xhr:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
            
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(error_url or request.url) 