'''# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_key: str
    azure_openai_deployment: str  # name of the deployment in Azure
    azure_openai_api_version: str = "2024-08-01-preview"  # adjust if needed
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()

# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
#from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    azure_openai_endpoint: str = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = Field(..., env="AZURE_OPENAI_KEY")
    azure_openai_deployment: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_version: str = Field("2024-10-01", env="AZURE_OPENAI_API_VERSION")
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()'''

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    azure_openai_endpoint: str = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = Field(..., env="AZURE_OPENAI_API_KEY")
    azure_openai_deployment: str = Field(..., env="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_version: str = Field("2024-08-01-preview", env="AZURE_OPENAI_API_VERSION")
    host: str = "0.0.0.0"
    port: int = 8000
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

