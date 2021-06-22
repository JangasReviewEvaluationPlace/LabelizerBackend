import os
from dotenv import load_dotenv
from flask_restx import Api

load_dotenv()

POSTGRES_CONFIGS = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DATABASE"),
    "port": os.getenv("POSTGRES_PORT"),
}

api = Api(
    version="0.1",
    title="Labelizer",
    description="Backend for Labeling relevant data for NLP."
)


class BaseConfigs:
    """Base Configs."""

    DEBUG = True
