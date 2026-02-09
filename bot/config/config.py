from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class BotSettings(BaseSettings):
    token: SecretStr
    ADMIN_IDS: list[int]

class PostgresSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    class Config:
        env_file = ".env"

class LogSettings(BaseSettings):
    log_level: str
    log_format: str
    class Config:
        env_file = ".env"
   
class Settings(BaseSettings):
    bot = BotSettings()
    postgres = PostgresSettings()
    log = LogSettings()

    @property
    def get_async_url(self) -> str:
        p = self.postgres
        return f"postgresql+asyncpg://{p.db_user}:{p.db_pass}@{p.db_host}:{p.db_port}/{p.db_name}"
    
    class Config:
        env_file = ".env"

settings = Settings()