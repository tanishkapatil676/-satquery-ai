import os
from pathlib import Path
from satquery.core.exceptions import ValidationError
from satquery.core.config import settings

class FileValidator:
    @staticmethod
    def validate(file_path: str) -> None:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            raise ValidationError(f"File not found or unreadable: {file_path}", code="FILE_NOT_FOUND")
        
        if path.suffix.lower() not in settings.satquery_allowed_raster_extensions:
            raise ValidationError(f"Unsupported file extension: {path.suffix}", code="UNSUPPORTED_EXTENSION")
        
        file_size = path.stat().st_size
        if file_size == 0:
            raise ValidationError("File is empty", code="EMPTY_FILE")
        
        if file_size > settings.satquery_max_upload_bytes:
            raise ValidationError(f"File size exceeds maximum limit of {settings.satquery_max_upload_bytes} bytes", code="FILE_TOO_LARGE")
