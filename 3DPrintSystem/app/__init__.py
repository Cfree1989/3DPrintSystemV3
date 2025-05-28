from flask import Flask
from .config import Config
from .extensions import db, migrate
from .models import Job, Event

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def hello():
        return "Hello, World! Database URI: {}".format(app.config.get('SQLALCHEMY_DATABASE_URI'))

    return app 