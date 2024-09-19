from flask import Flask
from config import Config
from extensions import db
from api import api_bp
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)