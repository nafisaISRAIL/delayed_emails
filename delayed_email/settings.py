from pydantic_settings import BaseSettings


class MongoDbSettings(BaseSettings):
    uri: str
    db_name: str


class RabbitmqSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: int
    routing_key: str = "email_sender"


class SMTPSetting(BaseSettings):
    server: str
    port: int
    username: str
    password: str


class Settings(BaseSettings):
    log_level: str = "INFO"
    mongodb: MongoDbSettings
    rabbitmq: RabbitmqSettings
    smtp: SMTPSetting

    class Config:
        env_prefix = "delayed_email_"
        env_nested_delimiter = "__"


settings = Settings()
