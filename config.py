import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    
    # SQLite Database Config
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "database" / "olist.db"))
    
    # SQLCoder Model Settings
    SQLCODER_MODEL_NAME = os.environ.get("SQLCODER_MODEL_NAME", "def-gpt/SQLCoder-7B")
    USE_GPU = os.environ.get("USE_GPU", "False").lower() in ("true", "1", "t")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ":memory:" # Run tests on an in-memory database
