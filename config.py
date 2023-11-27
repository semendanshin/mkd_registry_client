from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    dadata_token: SecretStr
    dadata_secret: SecretStr
    db_url: SecretStr
    postgres_password: SecretStr
    EGRN_REQUESTS_API_HOST: str


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
