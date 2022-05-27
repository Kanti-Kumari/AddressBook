#Standard Modules/Libs
import pathlib
from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import Optional


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///AddressBook.db"

    class Config:
        case_sensitive = True


settings = Settings()