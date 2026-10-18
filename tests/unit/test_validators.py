import pytest
import numpy as np
import rasterio
from rasterio.transform import from_origin
from src.satquery.core.exceptions import ValidationError
from src.satquery.validation.file_validator import FileValidator
from src.satquery.validation.raster_validator import RasterValidator

@pytest.fixture
def synthetic_geotiff(tmp_path):
    filepath = tmp_path / "test_raster.tif"
    transform = from_origin(0.0, 10.0, 1.0, 1.0)
    data = np.ones((1, 10, 10), dtype=np.uint8)
    
    with rasterio.open(
        filepath,
        'w',
        driver='GTiff',
        height=10,
        width=10,
        count=1,
        dtype=data.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(data)
    return str(filepath)

def test_file_validator_success(synthetic_geotiff):
    # Should not raise exception
    FileValidator.validate(synthetic_geotiff)

def test_file_validator_missing():
    with pytest.raises(ValidationError) as exc:
        FileValidator.validate("non_existent_file.tif")
    assert exc.value.code == "FILE_NOT_FOUND"

def test_raster_validator_success(synthetic_geotiff):
    meta = RasterValidator.validate_and_extract(synthetic_geotiff)
    assert meta.width == 10
    assert meta.height == 10
    assert meta.count == 1
    assert "EPSG:4326" in meta.crs
