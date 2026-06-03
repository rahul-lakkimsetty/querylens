import os
from flask import Flask
from config import Config

def create_app(config_class=Config):
    """
    Flask Application Factory.
    Initializes and configures the application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register web and API routes blueprint
    from .routes import bp
    app.register_blueprint(bp)
    
    return app
