from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "job-search"
    environment: str = "development"
    debug: bool = True


settings = Settings()
