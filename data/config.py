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
    SPREADSHEET_ID: Optional[str]
    SERVICE_ACCOUNT_EMAIL: Optional[str]
    GOOGLE_API_KEY: Optional[str]
    GOOGLE_APP_NAME: Optional[str]
    SERVICE_CREDS: Optional[str]


    class Config:
        env_prefix = 'HACKATHON_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
