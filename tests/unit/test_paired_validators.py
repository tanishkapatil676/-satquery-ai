
import pytest

from satquery.core.exceptions import ValidationError
from satquery.schemas.raster import (
    RasterMetadataSchema,
    RasterBoundsSchema,
)
from satquery.schemas.assets import AssetManifest, ProcessingRecord
from satquery.validation.temporal_validator import TemporalValidator
from satquery.validation.alignment_validator import AlignmentValidator


@pytest.fixture
def base_meta():
    return RasterMetadataSchema(
        driver="GTiff",
        width=10,
        height=10,
        count=1,
        crs="EPSG:4326",
        bounds=RasterBoundsSchema(
            left=0.0,
            bottom=0.0,
            right=1.0,
            top=1.0,
        ),
        res=[0.1, 0.1],
        nodata=None,
        dtypes=["uint8"],
    )


def test_temporal_validator_success(base_meta):
    result = TemporalValidator.validate_bitemporal_compatibility(
        base_meta, base_meta, "2026-01-01", "2026-06-01"
    )
    assert result["status"] == "compatible"
    assert result["temporal_status"] == "distinct_timestamps"


def test_temporal_validator_identical_timestamps(base_meta):
    with pytest.raises(ValidationError) as exc:
        TemporalValidator.validate_bitemporal_compatibility(
            base_meta, base_meta, "2026-01-01", "2026-01-01"
        )
    assert exc.value.code == "IDENTICAL_TIMESTAMPS"


def test_temporal_validator_missing_timestamps(base_meta):
    result = TemporalValidator.validate_bitemporal_compatibility(
        base_meta, base_meta
    )
    assert result["temporal_status"] == "missing_timestamps"


def test_alignment_validator_success(base_meta):
    result = AlignmentValidator.validate_spatial_alignment(
        base_meta, base_meta
    )
    assert result["alignment_status"] == "grid_compatible"


def test_alignment_validator_crs_mismatch(base_meta):
    meta_b = base_meta.model_copy(update={"crs": "EPSG:3857"})

    with pytest.raises(ValidationError) as exc:
        AlignmentValidator.validate_spatial_alignment(base_meta, meta_b)

    assert exc.value.code == "CRS_MISMATCH"


def test_asset_manifest_defaults():
    manifest = AssetManifest(
        source_filename="image.tif",
        storage_key="assets/example.tif",
    )
    assert manifest.asset_id
    assert manifest.status == "staged"
    assert manifest.processing == ()


def test_processing_record():
    record = ProcessingRecord(
        operation="select_bands",
        parameters={"bands": "1,2,3"},
    )
    assert record.operation == "select_bands"
