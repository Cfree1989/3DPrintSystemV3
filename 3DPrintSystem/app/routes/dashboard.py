from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        staff_password = current_app.config.get('STAFF_PASSWORD', 'Fabrication')
        if password == staff_password:
            session['staff_logged_in'] = True
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

# Example protected route
@bp.route('/')
def index():
    if not session.get('staff_logged_in'):
        return redirect(url_for('dashboard.login'))
    return render_template('dashboard/index.html') 