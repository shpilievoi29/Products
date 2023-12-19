import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, PositiveInt, RedisDsn, validator
from pydantic_settings import BaseSettings

from .validators import PostgresDsn


class Settings(BaseSettings):
    ###########
    # PROJECT #
    ###########
    PROJECT_NAME: str = "Products"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "very_secret_key")
    HTTP_SERVER: AnyHttpUrl
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", True)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ############
    # DATABASE #
    ############
    DB_SERVER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_SERVER"),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
