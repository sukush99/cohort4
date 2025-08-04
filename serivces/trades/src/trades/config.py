from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./settings.env',
        env_file_encoding='utf-8',
    )

    broker_address: str 
    kafka_topic_name: str 


config = Config()