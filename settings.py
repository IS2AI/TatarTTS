import sys
from pathlib import Path

from loguru import logger
from pydantic import Field, field_validator, BaseModel
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class HostPort(BaseModel):
    host: str
    port: int

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)


class UserPass(BaseModel):
    username: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).with_name('.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='_',
    )
    project_folder: Path = Field(Path(__file__).parent)
    storage_folder: Path = Field(alias='STORAGE_DIR')

    # noinspection PyMethodParameters
    @field_validator('storage_folder')
    def check_folder(cls, v):
        assert v.exists()
        return v

    @field_validator('storage_folder')
    def init_input_folder(cls, v, info: ValidationInfo):
        if v is None:
            v = info.data['storage_folder'] / info.field_name.replace('_folder', '')
            assert v.exists, f"Input folder {v} does not exist."
        return v


settings = Settings()

logger.remove()
logger.add(sys.stdout, colorize=True, format="{level.icon}|<level>{message}</level>")
