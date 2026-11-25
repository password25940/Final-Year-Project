import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    ALLOWED_PRN_START = 23021351242001
    ALLOWED_PRN_END = 23021351242538
    DEFAULT_STUDENT_PASSWORD = "123456"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{Path(__file__).with_name('student_feedback.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
