import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from satquery.core.config import Settings
from satquery.core.exceptions import RasterReadError
from satquery.ingestion.raster_reader import RasterReader


@pytest.fixture
def sample_tif(tmp_path):
    filepath = tmp_path / "sample.tif"
    transform = from_origin(0.0, 10.0, 1.0, 1.0)

    data = np.ones((2, 5, 5), dtype=np.float32)
    data[0, 2, 2] = np.nan

    with rasterio.open(
        filepath,
        "w",
        driver="GTiff",
        height=5,
        width=5,
        count=2,
        dtype="float32",
        crs="EPSG:4326",
        transform=transform,
        nodata=np.nan,
    ) as dst:
        dst.write(data)

    return filepath


def test_read_raster_success(sample_tif):
    data, meta = RasterReader.read_raster(sample_tif)

    assert data.shape == (2, 5, 5)
    assert data.dtype == np.float32
    assert meta.width == 5
    assert meta.height == 5
    assert meta.count == 2
    assert np.isnan(data[0, 2, 2])


def test_read_raster_missing_file():
    with pytest.raises(RasterReadError) as exc:
        RasterReader.read_raster("non_existent_raster.tif")

    assert exc.value.code == "FILE_NOT_FOUND"


def test_read_raster_pixel_limit(sample_tif):
    app_settings = Settings(satquery_max_raster_pixels=10)

    with pytest.raises(Exception) as exc:
        RasterReader.read_raster(sample_tif, app_settings)

    assert getattr(exc.value, "code", None) == "PIXEL_LIMIT_EXCEEDED"
