from pydantic_settings import SettingsConfigDict,BaseSettings
from pydantic import SecretStr

class AuthSettings(BaseSettings):
    secret_key : SecretStr 
    algorithm : str = "Hs256"
    access_token_expiry_minutes : int=30
    

    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding= "utf-8",
        extra="ignore"
    )

auth_settings = AuthSettings()

