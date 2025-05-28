from flask import Flask
from .config import Config
from .extensions import db, migrate
from .models import Job, Event
from .routes.dashboard import bp as dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(dashboard_bp)

    # Ensure secret key is set for sessions
    if not app.secret_key:
        app.secret_key = app.config.get('SECRET_KEY', 'dev')

    @app.route('/')
    def hello():
        return "Hello, World! Database URI: {}".format(app.config.get('SQLALCHEMY_DATABASE_URI'))

    return app 