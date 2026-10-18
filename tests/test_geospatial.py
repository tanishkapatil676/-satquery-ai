import numpy as np
from satquery.core.geospatial import GeospatialEngine


def test_calculate_ndvi():
    red = np.array([[100.0, 50.0]], dtype=np.float32)
    nir = np.array([[300.0, 150.0]], dtype=np.float32)

    ndvi = GeospatialEngine.calculate_ndvi(red, nir)

    expected = np.array([[0.5, 0.5]], dtype=np.float32)
    assert np.allclose(ndvi, expected)


def test_calculate_ndvi_zero_denominator():
    red = np.array([[0.0]], dtype=np.float32)
    nir = np.array([[0.0]], dtype=np.float32)

    ndvi = GeospatialEngine.calculate_ndvi(red, nir)
    assert np.isfinite(ndvi).all()
    assert ndvi[0, 0] == 0.0
