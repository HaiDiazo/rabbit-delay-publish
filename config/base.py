from pydantic import BaseSettings


class Settings(BaseSettings):
    SASMAKA_BROKER_HOST: str
    SASMAKA_BROKER_PORT: str
    SASMAKA_BROKER_USER: str
    SASMAKA_BROKER_PASS: str
    SASMAKA_BROKER_VHOST: str
    SASMAKA_BROKER_EXCHANGE: str

    class Config:
        env_file = ".env"


settings = Settings()
