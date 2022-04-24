from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    def __init__(self):
        super().__init__()

    PROJECT_NAME: str = 'Hackathon'
    LOGS_BASE_PATH: str = ''
    REDIS: dict = dict()
    TG_TOKEN: Optional[str]
    ADMINS: list = []

    WEBAPP_HOST: str
    WEBAPP_PATH: str
    WEBAPP_PORT: str

    WEBHOOK_PATH: str
    WEBHOOK_URL: str

    class Config:
        env_prefix = 'HACKATHON_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
