from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import uuid
import os
from datetime import datetime
from app.extensions import db
from app.models.job import Job
from app.models.event import Event
from app.services.file_service import save_uploaded_file
from app.utils.form_handler import FormHandler
from app.utils.validation import validate_required, validate_email, validate_file_required, ValidationError

bp = Blueprint('main', __name__)

def process_submission(form_data):
    """
    Handles the core logic of processing a validated form submission.
    This includes saving the file, creating Job and Event records,
    and committing them to the database.
    """
    try:
        uploaded_file = request.files.get('file')
        
        # Prepare data for file service
        file_service_data = {
            'studentName': form_data.get('student_name'),
            'studentEmail': form_data.get('student_email'),
            'discipline': form_data.get('discipline'),
            'classNumber': form_data.get('class_number'),
            'printMethod': form_data.get('print_method'),
            'colorPreference': form_data.get('color'),
            'printer': form_data.get('printer'),
            'minChargeConsent': form_data.get('acknowledged_minimum_charge')
        }

        display_name, file_path, metadata_path = save_uploaded_file(uploaded_file, file_service_data)

        if not display_name:
            # The file service returns the error message in the file_path variable on failure
            raise Exception(f"File upload failed: {file_path}")

        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            student_name=form_data['student_name'],
            student_email=form_data['student_email'],
            discipline=form_data['discipline'],
            class_number=form_data['class_number'],
            original_filename=uploaded_file.filename,
            display_name=display_name,
            file_path=file_path,
            metadata_path=metadata_path,
            status='UPLOADED',
            printer=form_data['printer'],
            color=form_data['color'],
            material=form_data['print_method'],
            acknowledged_minimum_charge=(form_data.get('acknowledged_minimum_charge') == 'yes'),
            student_confirmed=False,
            last_updated_by='student',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        event = Event(
            job_id=job_id,
            event_type='JobCreated',
            triggered_by='student',
            details={
                'student_name': form_data['student_name'],
                'student_email': form_data['student_email'],
                'original_filename': uploaded_file.filename,
                'display_name': display_name,
                'print_method': form_data['print_method'],
                'color': form_data['color'],
                'printer': form_data['printer']
            },
            timestamp=datetime.utcnow()
        )

        db.session.add(job)
        db.session.add(event)
        
        current_app.logger.info(f"New job created: {job_id[:8]} by {form_data['student_email']}")
        
        return {'success': True, 'job_id': job_id}

    except Exception as e:
        current_app.logger.error(f"Error in process_submission: {str(e)}")
        return {'success': False, 'error': str(e)}

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        schema = {
            'student_name': [
                lambda v, f: validate_required(v, f, 'Student Name')
            ],
            'student_email': [
                lambda v, f: validate_required(v, f, 'Student Email'),
                lambda v, f: validate_email(v, f, 'Student Email')
            ],
            'discipline': [
                lambda v, f: validate_required(v, f, 'Discipline')
            ],
            'class_number': [
                lambda v, f: validate_required(v, f, 'Class Number')
            ],
            'print_method': [
                lambda v, f: validate_required(v, f, 'Print Method')
            ],
            'color': [
                lambda v, f: validate_required(v, f, 'Color')
            ],
            'printer': [
                lambda v, f: validate_required(v, f, 'Printer')
            ],
            'acknowledged_minimum_charge': [
                lambda v, f: validate_required(v, f, 'Minimum Charge Consent'),
                lambda v, f: None if v == 'yes' else flash('You must acknowledge the minimum charge policy.', 'error')
            ],
            'file': [
                lambda v, f: validate_file_required(request.files.get(f), f, 'File Upload')
            ]
        }
        
        return FormHandler.handle_form_submission(
            schema=schema,
            process_data_func=process_submission,
            success_url_func=lambda result: url_for('main.submit_success', job_id=result['job_id'][:8]),
            error_template='student/submission/submit.html'
        )

    # GET request - show the form
    return render_template('student/submission/submit.html')

@bp.route('/submit/success')
def submit_success():
    job_id = request.args.get('job_id')
    if not job_id:
        flash('Invalid success page access.', 'error')
        return redirect(url_for('main.submit'))
    
    return render_template('student/submission/submit_success.html', job_id=job_id) 