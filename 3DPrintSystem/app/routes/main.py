from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import uuid
import os
from datetime import datetime
from app.extensions import db
from app.models.job import Job
from app.models.event import Event
from app.services.file_service import save_uploaded_file

bp = Blueprint('main', __name__)

@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            # Get uploaded file
            uploaded_file = request.files.get('file')
            if not uploaded_file or uploaded_file.filename == '':
                flash('Please select a file to upload.', 'error')
                return render_template('student/submission/submit.html')
            
            # Prepare form data for file service
            form_data = {
                'studentName': request.form.get('student_name', '').strip(),
                'studentEmail': request.form.get('student_email', '').strip(), 
                'discipline': request.form.get('discipline', ''),
                'classNumber': request.form.get('class_number', '').strip(),
                'printMethod': request.form.get('print_method', ''),
                'colorPreference': request.form.get('color', ''),
                'printer': request.form.get('printer', ''),
                'minChargeConsent': request.form.get('acknowledged_minimum_charge', '')
            }
            
            # Validate required fields
            required_fields = ['studentName', 'studentEmail', 'discipline', 'classNumber', 
                             'printMethod', 'colorPreference', 'printer', 'minChargeConsent']
            
            for field in required_fields:
                if not form_data.get(field):
                    flash(f'Please fill in all required fields. Missing: {field.replace("_", " ").title()}', 'error')
                    return render_template('student/submission/submit.html')
            
            # Validate minimum charge consent
            if form_data['minChargeConsent'].lower() != 'yes':
                flash('You must acknowledge the minimum charge policy to proceed.', 'error')
                return render_template('student/submission/submit.html')
            
            # Process file upload
            display_name, file_path, metadata_path = save_uploaded_file(uploaded_file, form_data)
            
            if not display_name:
                # file_path contains error message when display_name is None
                flash(f'File upload failed: {file_path}', 'error')
                return render_template('student/submission/submit.html')
            
            # Create database job record
            job_id = str(uuid.uuid4())
            
            job = Job(
                id=job_id,
                student_name=form_data['studentName'],
                student_email=form_data['studentEmail'],
                discipline=form_data['discipline'],
                class_number=form_data['classNumber'],
                original_filename=uploaded_file.filename,
                display_name=display_name,
                file_path=file_path,
                metadata_path=metadata_path,
                status='UPLOADED',
                printer=form_data['printer'],
                color=form_data['colorPreference'],
                material=form_data['printMethod'],  # Map printMethod to material
                acknowledged_minimum_charge=True,
                student_confirmed=False,
                last_updated_by='student',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Create JobCreated event
            event = Event(
                job_id=job_id,
                event_type='JobCreated',
                triggered_by='student',
                details={
                    'student_name': form_data['studentName'],
                    'student_email': form_data['studentEmail'],
                    'original_filename': uploaded_file.filename,
                    'display_name': display_name,
                    'print_method': form_data['printMethod'],
                    'color': form_data['colorPreference'],
                    'printer': form_data['printer']
                },
                timestamp=datetime.utcnow()
            )
            
            # Save to database
            db.session.add(job)
            db.session.add(event)
            db.session.commit()
            
            current_app.logger.info(f"New job created: {job_id[:8]} by {form_data['studentEmail']}")
            
            # Redirect to success page
            return redirect(url_for('main.submit_success', job_id=job_id[:8]))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error processing submission: {str(e)}")
            flash('An unexpected error occurred. Please try again or contact support.', 'error')
            return render_template('student/submission/submit.html')
    
    # GET request - show the form
    return render_template('student/submission/submit.html')

@bp.route('/submit/success')
def submit_success():
    job_id = request.args.get('job_id')
    if not job_id:
        flash('Invalid success page access.', 'error')
        return redirect(url_for('main.submit'))
    
    return render_template('student/submission/submit_success.html', job_id=job_id) 