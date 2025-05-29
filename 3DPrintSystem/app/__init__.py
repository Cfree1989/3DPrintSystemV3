from flask import Flask, redirect, url_for
import os
from .config import Config
from .extensions import db, migrate
from .models import Job, Event
from .routes.dashboard import bp as dashboard_bp
from .routes.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    
    # Validate configuration before proceeding
    Config.validate_required_config()
    app.config.from_object(Config)

    # Ensure storage directories exist
    storage_dirs = [
        app.config['APP_STORAGE_ROOT'],
        app.config['UPLOAD_FOLDER'],
        os.path.join(app.config['APP_STORAGE_ROOT'], 'Pending'),
        os.path.join(app.config['APP_STORAGE_ROOT'], 'ReadyToPrint'),
        os.path.join(app.config['APP_STORAGE_ROOT'], 'Printing'),
        os.path.join(app.config['APP_STORAGE_ROOT'], 'Completed'),
        os.path.join(app.config['APP_STORAGE_ROOT'], 'PaidPickedUp'),
        os.path.join(app.config['APP_STORAGE_ROOT'], 'thumbnails')
    ]
    
    for directory in storage_dirs:
        os.makedirs(directory, exist_ok=True)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    # Ensure secret key is set for sessions
    if not app.secret_key:
        app.secret_key = app.config.get('SECRET_KEY', 'dev')

    @app.route('/')
    def index():
        """Redirect root to submit form - main entry point for students"""
        return redirect(url_for('main.submit'))

    return app 