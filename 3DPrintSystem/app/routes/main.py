from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/submit', methods=['GET'])
def submit():
    return render_template('main/submit.html') 