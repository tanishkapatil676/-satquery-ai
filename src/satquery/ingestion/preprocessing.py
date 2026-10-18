from typing import Sequence

import numpy as np

from satquery.core.exceptions import ValidationError


class RasterPreprocessor:
    @staticmethod
    def select_bands(
        data: np.ndarray,
        band_indices: Sequence[int],
    ) -> np.ndarray:
        """Select bands from a (bands, height, width) array."""

        if data.ndim != 3:
            raise ValidationError(
                "Input must have shape (bands, height, width).",
                code="INVALID_DIMENSIONS",
            )

        if len(band_indices) == 0:
            raise ValidationError(
                "At least one band must be selected.",
                code="EMPTY_SELECTION",
            )

        total_bands = data.shape[0]

        for idx in band_indices:
            if (
                not isinstance(idx, (int, np.integer))
                or isinstance(idx, (bool, np.bool_))
                or idx < 0
                or idx >= total_bands
            ):
                raise ValidationError(
                    f"Band index {idx} is out of bounds.",
                    code="OUT_OF_BOUNDS_BAND",
                )

        return data[list(band_indices), :, :]

    @staticmethod
    def normalize_finite_values(data: np.ndarray) -> np.ndarray:
        """Normalize each band independently to [0, 1], preserving NaNs."""

        if data.ndim != 3:
            raise ValidationError(
                "Input must have shape (bands, height, width).",
                code="INVALID_DIMENSIONS",
            )

        output = data.astype(np.float32, copy=True)

        for i in range(output.shape[0]):
            band = output[i]
            finite_mask = np.isfinite(band)

            if not np.any(finite_mask):
                # No valid pixels in this band.
                output[i] = 0.0
                continue

            finite_values = band[finite_mask]
            min_value = np.min(finite_values)
            max_value = np.max(finite_values)

            if max_value == min_value:
                band[finite_mask] = 0.0
            else:
                band[finite_mask] = (
                    (finite_values - min_value)
                    / (max_value - min_value)
                )

            output[i] = band

        return output

    @staticmethod
    def replace_invalid_pixels(
        data: np.ndarray,
        fill_value: float = 0.0,
    ) -> np.ndarray:
        """Replace NaN and infinite pixels with a finite value."""

        if data.ndim != 3:
            raise ValidationError(
                "Input must have shape (bands, height, width).",
                code="INVALID_DIMENSIONS",
            )

        if (
            not isinstance(fill_value, (int, float, np.number))
            or not np.isfinite(fill_value)
        ):
            raise ValidationError(
                "Fill value must be finite and numeric.",
                code="INVALID_FILL_VALUE",
            )

        output = data.astype(np.float32, copy=True)
        output[~np.isfinite(output)] = float(fill_value)

        return output
