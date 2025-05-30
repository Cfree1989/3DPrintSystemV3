from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from app.models.job import Job

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