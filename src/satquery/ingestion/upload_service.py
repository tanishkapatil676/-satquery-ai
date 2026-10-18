import uuid
from pathlib import Path
from typing import Iterable, Tuple

from satquery.core.config import Settings, settings
from satquery.core.exceptions import ValidationError, SatQueryError


class UploadService:
    @staticmethod
    def stage_upload(
        chunks: Iterable[bytes],
        original_filename: str,
        app_settings: Settings = settings,
    ) -> Tuple[str, Path]:
        """Stage uploaded chunks with size checks and failure cleanup."""

        if not original_filename or not original_filename.strip():
            raise ValidationError(
                "Original filename is missing or empty.",
                code="INVALID_FILENAME",
            )

        ext = Path(original_filename).suffix.lower()

        allowed_extensions = [
            item.lower()
            for item in app_settings.satquery_allowed_raster_extensions
        ]

        if ext not in allowed_extensions:
            raise ValidationError(
                f"Unsupported file extension: {ext}",
                code="UNSUPPORTED_EXTENSION",
            )

        asset_id = str(uuid.uuid4())
        staged_path = (
            Path(app_settings.satquery_temp_dir)
            / f"{asset_id}{ext}"
        )

        staged_path.parent.mkdir(parents=True, exist_ok=True)

        total_bytes = 0
        has_data = False

        try:
            with staged_path.open("wb") as file:
                for chunk in chunks:
                    if not chunk:
                        continue

                    if not isinstance(chunk, bytes):
                        raise ValidationError(
                            "Upload chunks must be bytes.",
                            code="INVALID_CHUNK",
                        )

                    total_bytes += len(chunk)

                    if total_bytes > app_settings.satquery_max_upload_bytes:
                        raise ValidationError(
                            "Upload exceeds the configured size limit.",
                            code="FILE_TOO_LARGE",
                        )

                    file.write(chunk)
                    has_data = True

            if not has_data or total_bytes == 0:
                raise ValidationError(
                    "Uploaded file is empty.",
                    code="EMPTY_FILE",
                )

        except Exception as exc:
            try:
                staged_path.unlink(missing_ok=True)
            except OSError:
                pass

            if isinstance(exc, SatQueryError):
                raise

            raise ValidationError(
                f"Filesystem error during upload staging: {exc}",
                code="STAGING_ERROR",
            ) from exc

        return asset_id, staged_path
