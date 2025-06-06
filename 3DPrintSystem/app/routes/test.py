from flask import Blueprint, render_template, request, jsonify
from app.utils.validation import validate_required, validate_email, validate_length, validate_number
from app.utils.form_handler import FormHandler

bp = Blueprint('test', __name__)

@bp.route('/validation-test')
def validation_test():
    """Render the validation test form"""
    return render_template('test/validation_test.html')

@bp.route('/validate-form', methods=['POST'])
def validate_form():
    """Handle form submission with validation"""
    # Define validation schema
    schema = {
        'name': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_length(v, f, min_length=2, max_length=50)
        ],
        'email': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_email(v, f)
        ],
        'age': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_number(v, f, min_value=18, max_value=120)
        ],
        'message': [
            lambda v, f: validate_required(v, f),
            lambda v, f: validate_length(v, f, min_length=10, max_length=500)
        ],
        'terms': [
            lambda v, f: validate_required(v, f)
        ]
    }
    
    # Use FormHandler to process the submission
    return FormHandler.handle_form_submission(
        schema=schema,
        success_url='test.validation_test',
        success_message='Form submitted successfully!',
        process_data=lambda data: {
            **data,
            'processed': True  # Example of data processing
        }
    ) 