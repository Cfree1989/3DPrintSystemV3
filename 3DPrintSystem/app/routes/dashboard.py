from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from app.models.job import Job
from app.extensions import db

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
    return render_template('dashboard/login.html')

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
        
        return render_template('dashboard/index.html', 
                             jobs=jobs, 
                             stats=stats, 
                             current_status=status,
                             tabs=tabs)
                             
    except Exception as e:
        current_app.logger.error(f"Error loading dashboard: {str(e)}")
        # Graceful degradation - return empty state instead of crash
        return render_template('dashboard/index.html', 
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