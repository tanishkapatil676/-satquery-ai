from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    satquery_app_name: str = "SatQuery AI"
    satquery_environment: str = "development"
    satquery_debug: bool = False
    satquery_log_level: str = "INFO"
    satquery_max_upload_bytes: int = 52428800  # 50MB
    satquery_max_raster_pixels: int = 100000000
    satquery_allowed_raster_extensions: List[str] = [".tif", ".tiff"]
    satquery_temp_dir: str = "/tmp/satquery"
    satquery_default_model_id: str = "UNCONFIGURED"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
