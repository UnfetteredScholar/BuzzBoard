import logging
import logging.handlers
import os
from typing import Any, List

from pydantic_settings import BaseSettings


def configure_logging():
    """Configures logging for the API"""

    if not os.path.isdir("./logs"):
        os.mkdir("./logs")

    handler = logging.handlers.TimedRotatingFileHandler(
        filename="./logs/buzz_board.log",
        when="midnight",
        interval=1,
        backupCount=7,
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s  - %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)


class Settings(BaseSettings):
    APP_NAME: str = "BuzzBoard API"
    VERSION: str = "1.0"
    RELEASE_ID: str = "1.0"
    API_V1_STR: str = "/api/v1"
    DB_NAME: str = "buzz-board-database"
    BACKEND_CORS_ORIGINS: List[str] = os.environ.get(
        "CORS_ORIGINS", "*"
    ).split(",")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_DAYS: str = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")
    MONGO_DB_URI: str = os.getenv("MONGODB_URI")

    def __init__(self, **values: Any):
        super().__init__(**values)


settings = Settings()
configure_logging()
