import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configure app from environment or defaults
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev_secret_key"),
        DATABASE=os.path.join(app.root_path, "../database/olist.db")
    )
    
    # Register blueprints/routes
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
