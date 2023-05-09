"""For loading and validating configs"""
import os
from typing import Literal
from pydantic import BaseSettings, MongoDsn, FilePath, SecretStr

__env_mode = os.getenv("ENVIRONMENT")
__base_dir = os.path.abspath(os.path.dirname(__file__))
__files = [".env"]

if __env_mode == "production":
    __files = [".env.prod.local", ".env.local", ".env.prod"] + __files
else:
    __files = [".env.dev.local", ".env.local", ".env.dev"] + __files
    if not __env_mode:
        print("Could not identify environment ($ENVIRONMENT), assuming development")


class Settings(BaseSettings):
    PRIORITY_FLAG: Literal[
        ".env.dev.local", ".env.dev", ".env.local", ".env.prod.local", ".env.prod"
    ]
    MONGODB_URL: MongoDsn
    SECRET_KEY: SecretStr
    MODEL: FilePath
    MLB: FilePath


settings = Settings(
    _env_file=tuple(os.path.join(__base_dir, f"../{file}") for file in __files),
    _env_file_encoding="utf-8",
)

print("Priority environment:", settings.PRIORITY_FLAG)
