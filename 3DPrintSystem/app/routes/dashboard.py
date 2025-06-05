from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from app.models.job import Job
from app.models.event import Event
from app.extensions import db
import os
from datetime import datetime

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(f):
    """Decorator for protecting dashboard routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('staff_logged_in'):
            return redirect(url_for('dashboard.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        staff_password = current_app.config.get('STAFF_PASSWORD', 'Fabrication')
        if password == staff_password:
            session['staff_logged_in'] = True
            session.permanent = True  # Remember login
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('staff/auth/login.html')

@bp.route('/logout')
def logout():
    session.pop('staff_logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('dashboard.login'))

@bp.route('/')
@login_required
def index():
    """Main dashboard with status parameter routing"""
    status = request.args.get('status', 'UPLOADED').upper()
    valid_statuses = ['UPLOADED', 'PENDING', 'READYTOPRINT', 'PRINTING', 'COMPLETED', 'PAIDPICKEDUP', 'REJECTED']
    
    if status not in valid_statuses:
        status = 'UPLOADED'
    
    try:
        # Get jobs for selected status
        jobs = Job.query.filter_by(status=status).order_by(Job.created_at.desc()).all()
        
        # Calculate statistics for all tabs
        stats = {
            'uploaded': Job.query.filter_by(status='UPLOADED').count(),
            'pending': Job.query.filter_by(status='PENDING').count(),
            'ready': Job.query.filter_by(status='READYTOPRINT').count(),
            'printing': Job.query.filter_by(status='PRINTING').count(),
            'completed': Job.query.filter_by(status='COMPLETED').count(),
            'paidpickedup': Job.query.filter_by(status='PAIDPICKEDUP').count(),
            'rejected': Job.query.filter_by(status='REJECTED').count()
        }
        
        # Tab configuration
        tabs = {
            'UPLOADED': {'title': 'Uploaded', 'stat_key': 'uploaded'},
            'PENDING': {'title': 'Pending', 'stat_key': 'pending'},
            'READYTOPRINT': {'title': 'Ready to Print', 'stat_key': 'ready'},
            'PRINTING': {'title': 'Printing', 'stat_key': 'printing'},
            'COMPLETED': {'title': 'Completed', 'stat_key': 'completed'}, 
            'PAIDPICKEDUP': {'title': 'Picked Up', 'stat_key': 'paidpickedup'},
            'REJECTED': {'title': 'Rejected', 'stat_key': 'rejected'}
        }
        
        return render_template('staff/dashboard/index.html', 
                             jobs=jobs, 
                             stats=stats, 
                             current_status=status,
                             tabs=tabs)
                             
    except Exception as e:
        current_app.logger.error(f"Error loading dashboard: {str(e)}")
        # Graceful degradation - return empty state instead of crash
        return render_template('staff/dashboard/index.html', 
                             jobs=[], 
                             stats={},
                             current_status=status,
                             tabs={})

@bp.route('/api/stats')
@login_required
def api_stats():
    """Lightweight JSON API endpoint for auto-updating dashboard"""
    try:
        # Get current status parameter for job listing
        status = request.args.get('status', 'UPLOADED').upper()
        valid_statuses = ['UPLOADED', 'PENDING', 'READYTOPRINT', 'PRINTING', 'COMPLETED', 'PAIDPICKEDUP', 'REJECTED']
        
        if status not in valid_statuses:
            status = 'UPLOADED'
        
        # Calculate statistics for all tabs
        stats = {
            'uploaded': Job.query.filter_by(status='UPLOADED').count(),
            'pending': Job.query.filter_by(status='PENDING').count(),
            'ready': Job.query.filter_by(status='READYTOPRINT').count(),
            'printing': Job.query.filter_by(status='PRINTING').count(),
            'completed': Job.query.filter_by(status='COMPLETED').count(),
            'paidpickedup': Job.query.filter_by(status='PAIDPICKEDUP').count(),
            'rejected': Job.query.filter_by(status='REJECTED').count()
        }
        
        # Get jobs for current status with basic information needed for UI updates
        jobs = Job.query.filter_by(status=status).order_by(Job.created_at.desc()).all()
        
        # Convert jobs to lightweight JSON format
        jobs_data = []
        for job in jobs:
            job_data = {
                'id': job.id,
                'student_name': job.student_name,
                'student_email': job.student_email,
                'discipline': job.discipline,
                'class_number': job.class_number,
                'original_filename': job.original_filename,
                'display_name': job.display_name,
                'created_at': job.created_at.isoformat() if job.created_at else None,
                'printer': job.printer,
                'color': job.color,
                'material': job.material,
                'cost_usd': float(job.cost_usd) if job.cost_usd else None,
                'staff_viewed_at': job.staff_viewed_at.isoformat() if job.staff_viewed_at else None
            }
            jobs_data.append(job_data)
        
        return jsonify({
            'success': True,
            'stats': stats,
            'jobs': jobs_data,
            'current_status': status,
            'timestamp': Job.query.first().created_at.isoformat() if Job.query.first() else None
        })
        
    except Exception as e:
        current_app.logger.error(f"Error loading dashboard stats API: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to load dashboard statistics'
        }), 500 

@bp.route('/api/mark-reviewed/<job_id>', methods=['POST'])
@login_required
def mark_job_reviewed(job_id):
    """Mark a job as reviewed by staff"""
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
            
        # Get request data for audit trail (handle both JSON and non-JSON requests)
        request_data = {}
        try:
            if request.is_json:
                request_data = request.get_json() or {}
        except Exception:
            # Non-JSON request, use default values
            request_data = {'action': 'mark_reviewed_legacy'}
        
        # Update the staff_viewed_at timestamp
        from datetime import datetime
        job.staff_viewed_at = datetime.utcnow()
        job.last_updated_by = 'staff'
        db.session.commit()
        
        # Log audit trail
        current_app.logger.info(f"Job {job_id[:8]} marked as reviewed by staff - Action: {request_data.get('action', 'mark_reviewed')}")
        
        return jsonify({
            'success': True,
            'message': 'Job marked as reviewed'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error marking job {job_id[:8]} as reviewed: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to mark job as reviewed'
        }), 500 

@bp.route('/api/mark-unreviewed/<job_id>', methods=['POST'])
@login_required
def mark_job_unreviewed(job_id):
    """Mark a job as unreviewed (undo review action)"""
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
            
        # Get request data for audit trail (handle both JSON and non-JSON requests)
        request_data = {}
        try:
            if request.is_json:
                request_data = request.get_json() or {}
        except Exception:
            # Non-JSON request, use default values
            request_data = {'action': 'mark_unreviewed_legacy'}
        
        # Clear the staff_viewed_at timestamp to mark as unreviewed
        job.staff_viewed_at = None
        job.last_updated_by = 'staff'
        db.session.commit()
        
        # Log audit trail
        current_app.logger.info(f"Job {job_id[:8]} marked as unreviewed by staff - Action: {request_data.get('action', 'mark_unreviewed')}")
        
        return jsonify({
            'success': True,
            'message': 'Job marked as unreviewed'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error marking job {job_id[:8]} as unreviewed: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to mark job as unreviewed'
        }), 500

@bp.route('/api/approve-job/<job_id>', methods=['POST'])
@login_required
def approve_job(job_id):
    """Approve a job and move it to PENDING status"""
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
            
        # Validate job can be approved (must be UPLOADED)
        if job.status != 'UPLOADED':
            return jsonify({
                'success': False,
                'error': f'Job cannot be approved from {job.status} status'
            }), 400
        
        # Get approval data from request
        approval_data = request.get_json() or {}
        weight_g = approval_data.get('weight_g')
        time_hours = approval_data.get('time_hours')
        material = approval_data.get('material')
        notes = approval_data.get('notes', '')
        
        # Basic validation
        if not weight_g or not time_hours:
            return jsonify({
                'success': False,
                'error': 'Weight and time are required for approval'
            }), 400
        
        try:
            weight_g = float(weight_g)
            time_hours = float(time_hours)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Weight and time must be valid numbers'
            }), 400
        
        # Calculate cost based on material and weight
        cost_per_gram = 0.20 if material and 'resin' in material.lower() else 0.10
        calculated_cost = max(weight_g * cost_per_gram, 3.00)  # $3.00 minimum
        
        # Move file from Uploaded to Pending directory
        try:
            new_file_path, new_metadata_path = _move_file_between_status_dirs(
                job.file_path, 'Uploaded', 'Pending'
            )
        except Exception as e:
            current_app.logger.error(f"Failed to move file for job {job_id[:8]}: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to move job file'
            }), 500
        
        # Update job in database
        job.status = 'PENDING'
        job.weight_g = weight_g
        job.time_hours = time_hours
        job.material = material or job.material
        job.cost_usd = calculated_cost
        job.file_path = new_file_path
        if new_metadata_path:
            job.metadata_path = new_metadata_path
        job.last_updated_by = 'staff'
        job.staff_viewed_at = datetime.utcnow()  # Mark as reviewed during approval
        if notes:
            job.notes = f"{job.notes or ''}\n[APPROVAL] {notes}".strip()
        
        # Generate confirmation token for student
        from app.utils.tokens import generate_confirmation_token
        token, expiration = generate_confirmation_token(job.id)
        job.confirm_token = token
        job.confirm_token_expires = expiration
        
        # Create event log
        approval_event = Event(
            job_id=job.id,
            event_type='StaffApproved',
            details={
                'weight_g': weight_g,
                'time_hours': time_hours,
                'material': material,
                'cost_usd': float(calculated_cost),
                'staff_notes': notes
            },
            triggered_by='staff'
        )
        db.session.add(approval_event)
        
        db.session.commit()
        
        # Log success
        current_app.logger.info(f"Job {job_id[:8]} approved by staff - Weight: {weight_g}g, Time: {time_hours}h, Cost: ${calculated_cost:.2f}")
        
        return jsonify({
            'success': True,
            'message': f'Job approved successfully. Cost: ${calculated_cost:.2f}',
            'job_data': {
                'status': job.status,
                'cost_usd': float(calculated_cost),
                'weight_g': weight_g,
                'time_hours': time_hours
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error approving job {job_id[:8]}: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to approve job'
        }), 500

@bp.route('/api/reject-job/<job_id>', methods=['POST'])
@login_required
def reject_job(job_id):
    """Reject a job and move it to REJECTED status"""
    try:
        job = Job.query.filter_by(id=job_id).first()
        if not job:
            return jsonify({
                'success': False,
                'error': 'Job not found'
            }), 404
            
        # Validate job can be rejected (must be UPLOADED)
        if job.status != 'UPLOADED':
            return jsonify({
                'success': False,
                'error': f'Job cannot be rejected from {job.status} status'
            }), 400
        
        # Get rejection data from request
        rejection_data = request.get_json() or {}
        rejection_reasons = rejection_data.get('reasons', [])
        custom_reason = rejection_data.get('custom_reason', '')
        notes = rejection_data.get('notes', '')
        
        # Validate at least one reason is provided
        if not rejection_reasons and not custom_reason:
            return jsonify({
                'success': False,
                'error': 'At least one rejection reason must be provided'
            }), 400
        
        # Combine reasons
        all_reasons = rejection_reasons[:]
        if custom_reason:
            all_reasons.append(custom_reason)
        
        # Update job in database
        job.status = 'REJECTED'
        job.reject_reasons = all_reasons
        job.last_updated_by = 'staff'
        job.staff_viewed_at = datetime.utcnow()  # Mark as reviewed during rejection
        if notes:
            job.notes = f"{job.notes or ''}\n[REJECTION] {notes}".strip()
        
        # Create event log
        rejection_event = Event(
            job_id=job.id,
            event_type='JobRejected',
            details={
                'rejection_reasons': all_reasons,
                'staff_notes': notes
            },
            triggered_by='staff'
        )
        db.session.add(rejection_event)
        
        db.session.commit()
        
        # Log success
        current_app.logger.info(f"Job {job_id[:8]} rejected by staff - Reasons: {', '.join(all_reasons)}")
        
        return jsonify({
            'success': True,
            'message': 'Job rejected successfully',
            'job_data': {
                'status': job.status,
                'reject_reasons': all_reasons
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error rejecting job {job_id[:8]}: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to reject job'
        }), 500

def _move_file_between_status_dirs(current_path, from_status, to_status):
    """Move a file between status directories"""
    if not current_path or not os.path.exists(current_path):
        raise FileNotFoundError(f"Source file not found: {current_path}")
    
    # Get storage root from config
    storage_root = current_app.config.get('APP_STORAGE_ROOT', 'storage')
    
    # Extract filename
    filename = os.path.basename(current_path)
    
    # Create new path in target directory
    target_dir = os.path.join(storage_root, to_status)
    os.makedirs(target_dir, exist_ok=True)
    
    new_path = os.path.join(target_dir, filename)
    
    # Move the file
    os.rename(current_path, new_path)
    
    # Also move metadata file if it exists
    metadata_filename = os.path.splitext(filename)[0] + '.metadata.json'
    current_metadata_path = os.path.join(os.path.dirname(current_path), metadata_filename)
    new_metadata_path = None
    if os.path.exists(current_metadata_path):
        new_metadata_path = os.path.join(target_dir, metadata_filename)
        os.rename(current_metadata_path, new_metadata_path)

    return new_path, new_metadata_path
