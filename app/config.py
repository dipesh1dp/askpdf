from pydantic_settings import BaseSettings
from pydantic import Field 

class Settings(BaseSettings): 
    database_username: str = Field(alias="DATABASE_USERNAME")
    database_password: str = Field(alias="DATABASE_PASSWORD")
    database_port: str = Field(alias="DATABASE_PORT") 
    database_hostname: str = Field(alias="DATABASE_HOST") 
    database_name: str = Field(alias="DATABASE_NAME") 

    secret_key: str = Field(alias="SECRET_KEY") 
    algorithm: str = Field(alias="ALGORITHM") 
    acess_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES") 

    gemini_api_key: str = Field(alias="GEMINI_API_KEY")
    embedding_model: str = Field(alias="EMBEDDING_MODEL")

    chunk_size: int = Field(alias="CHUNK_SIZE")
    chunk_overlap: int = Field(alias="CHUNK_OVERLAP")

    poppler_path: str = Field(alias="POPPLER_PATH")

    class Config: 
        env_file = ".env" 


settings = Settings() 
