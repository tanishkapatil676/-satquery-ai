import numpy as np
import pytest

from satquery.core.exceptions import ValidationError
from satquery.ingestion.preprocessing import RasterPreprocessor


def test_select_bands():
    data = np.arange(24, dtype=np.float32).reshape(3, 2, 4)

    selected = RasterPreprocessor.select_bands(data, [0, 2])

    assert selected.shape == (2, 2, 4)
    np.testing.assert_array_equal(selected[0], data[0])
    np.testing.assert_array_equal(selected[1], data[2])


def test_select_bands_out_of_bounds():
    data = np.zeros((2, 2, 2), dtype=np.float32)

    with pytest.raises(ValidationError) as exc:
        RasterPreprocessor.select_bands(data, [5])

    assert exc.value.code == "OUT_OF_BOUNDS_BAND"


def test_select_bands_empty():
    data = np.zeros((2, 2, 2), dtype=np.float32)

    with pytest.raises(ValidationError) as exc:
        RasterPreprocessor.select_bands(data, [])

    assert exc.value.code == "EMPTY_SELECTION"


def test_normalize_finite_values():
    data = np.array(
        [[[1.0, 5.0], [10.0, np.nan]]],
        dtype=np.float32,
    )

    normalized = RasterPreprocessor.normalize_finite_values(data)

    assert normalized.shape == (1, 2, 2)
    assert np.isnan(normalized[0, 1, 1])
    assert normalized[0, 0, 0] == 0.0
    assert normalized[0, 1, 0] == 1.0


def test_normalize_constant_band():
    data = np.full((1, 2, 2), 7.0, dtype=np.float32)

    normalized = RasterPreprocessor.normalize_finite_values(data)

    np.testing.assert_array_equal(normalized, np.zeros_like(data))


def test_replace_invalid_pixels():
    data = np.array(
        [[[1.0, np.nan], [np.inf, -np.inf]]],
        dtype=np.float32,
    )

    cleaned = RasterPreprocessor.replace_invalid_pixels(data)

    assert np.all(np.isfinite(cleaned))
    assert cleaned[0, 0, 1] == 0.0
    assert cleaned[0, 1, 0] == 0.0


def test_replace_invalid_pixels_rejects_infinite_fill():
    data = np.zeros((1, 2, 2), dtype=np.float32)

    with pytest.raises(ValidationError) as exc:
        RasterPreprocessor.replace_invalid_pixels(data, np.inf)

    assert exc.value.code == "INVALID_FILL_VALUE"
