import pytest

from satquery.core.config import Settings
from satquery.core.exceptions import ValidationError
from satquery.ingestion.upload_service import UploadService


def test_stage_upload_success(tmp_path):
    app_settings = Settings(
        satquery_temp_dir=str(tmp_path / "uploads"),
        satquery_max_upload_bytes=1024,
    )

    asset_id, staged_path = UploadService.stage_upload(
        [b"chunk1", b"chunk2"],
        "test_image.tif",
        app_settings,
    )

    assert asset_id
    assert staged_path.exists()
    assert staged_path.suffix == ".tif"
    assert staged_path.read_bytes() == b"chunk1chunk2"


def test_stage_upload_unsupported_extension(tmp_path):
    app_settings = Settings(satquery_temp_dir=str(tmp_path))

    with pytest.raises(ValidationError) as exc:
        UploadService.stage_upload([b"data"], "document.pdf", app_settings)

    assert exc.value.code == "UNSUPPORTED_EXTENSION"


def test_stage_upload_empty(tmp_path):
    app_settings = Settings(satquery_temp_dir=str(tmp_path))

    with pytest.raises(ValidationError) as exc:
        UploadService.stage_upload([b"", b""], "empty.tif", app_settings)

    assert exc.value.code == "EMPTY_FILE"


def test_stage_upload_too_large_and_cleanup(tmp_path):
    app_settings = Settings(
        satquery_temp_dir=str(tmp_path),
        satquery_max_upload_bytes=5,
    )

    with pytest.raises(ValidationError) as exc:
        UploadService.stage_upload([b"abcdef"], "large.tif", app_settings)

    assert exc.value.code == "FILE_TOO_LARGE"
    assert list(tmp_path.iterdir()) == []
