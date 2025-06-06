from typing import Any, Dict, List, Optional, Union
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, errors: Optional[Dict[str, str]] = None):
        super().__init__(message)
        self.errors = errors or {}

def validate_required(value: Any, field_name: str) -> None:
    """Validate that a required field is not empty"""
    if value is None or value == '':
        raise ValidationError(f"{field_name} is required")

def validate_email(value: str, field_name: str) -> None:
    """Validate email format"""
    if not value:
        return
    import re
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_pattern, value):
        raise ValidationError(f"Invalid email format for {field_name}")

def validate_length(value: str, field_name: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> None:
    """Validate string length"""
    if not value:
        return
    if min_length is not None and len(value) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters")
    if max_length is not None and len(value) > max_length:
        raise ValidationError(f"{field_name} must be no more than {max_length} characters")

def validate_number(value: Union[int, float], field_name: str, min_value: Optional[Union[int, float]] = None, max_value: Optional[Union[int, float]] = None) -> None:
    """Validate number range"""
    if value is None:
        return
    try:
        num_value = float(value)
        if min_value is not None and num_value < min_value:
            raise ValidationError(f"{field_name} must be at least {min_value}")
        if max_value is not None and num_value > max_value:
            raise ValidationError(f"{field_name} must be no more than {max_value}")
    except ValueError:
        raise ValidationError(f"{field_name} must be a valid number")

def validate_file(file: Any, field_name: str, allowed_types: Optional[List[str]] = None, max_size_mb: Optional[int] = None) -> None:
    """Validate file upload"""
    if not file:
        return
    if allowed_types and file.content_type not in allowed_types:
        raise ValidationError(f"{field_name} must be one of: {', '.join(allowed_types)}")
    if max_size_mb and file.content_length > max_size_mb * 1024 * 1024:
        raise ValidationError(f"{field_name} must be less than {max_size_mb}MB")

def validate_form_data(schema: Dict[str, List[callable]]) -> Dict[str, Any]:
    """Validate form data against a schema"""
    errors = {}
    form_data = {}
    
    try:
        for field_name, validators in schema.items():
            value = request.form.get(field_name)
            if value is not None:
                form_data[field_name] = value
            
            try:
                for validator in validators:
                    validator(value, field_name)
            except ValidationError as e:
                errors[field_name] = str(e)
        
        if errors:
            raise ValidationError("Validation failed", errors)
        
        return form_data
    except ValidationError as e:
        if request.is_xhr:
            return jsonify({
                'success': False,
                'errors': e.errors
            }), 400
        raise BadRequest(str(e))

def validate_json_data(schema: Dict[str, List[callable]]) -> Dict[str, Any]:
    """Validate JSON data against a schema"""
    errors = {}
    json_data = {}
    
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("No JSON data provided")
        
        for field_name, validators in schema.items():
            value = data.get(field_name)
            if value is not None:
                json_data[field_name] = value
            
            try:
                for validator in validators:
                    validator(value, field_name)
            except ValidationError as e:
                errors[field_name] = str(e)
        
        if errors:
            raise ValidationError("Validation failed", errors)
        
        return json_data
    except ValidationError as e:
        if request.is_xhr:
            return jsonify({
                'success': False,
                'errors': e.errors
            }), 400
        raise BadRequest(str(e)) 