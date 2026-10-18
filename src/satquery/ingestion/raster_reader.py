from pathlib import Path
from typing import Tuple

import numpy as np
import rasterio

from satquery.core.config import Settings, settings
from satquery.core.exceptions import ValidationError, RasterReadError
from satquery.schemas.raster import RasterMetadataSchema
from satquery.validation.raster_validator import RasterValidator


class RasterReader:
    @staticmethod
    def read_raster(
        path: Path,
        app_settings: Settings = settings,
    ) -> Tuple[np.ndarray, RasterMetadataSchema]:
        """Read a raster into a band-first float32 array."""

        path_obj = Path(path)

        if not path_obj.exists() or not path_obj.is_file():
            raise RasterReadError(
                f"Raster file not found at path: {path_obj}",
                code="FILE_NOT_FOUND",
            )

        # Validate metadata before allocating the raster array.
        meta = RasterValidator.validate_and_extract(str(path_obj))

        total_pixels = meta.width * meta.height

        if total_pixels > app_settings.satquery_max_raster_pixels:
            raise ValidationError(
                "Raster pixel count exceeds the configured limit.",
                code="PIXEL_LIMIT_EXCEEDED",
            )

        try:
            with rasterio.open(path_obj) as src:
                masked_data = src.read(masked=True).astype(np.float32)

                # Convert masked/nodata cells to NaN in a normal ndarray.
                data = np.ma.filled(masked_data, np.nan).astype(
                    np.float32, copy=False
                )

                bands, height, width = data.shape

                if (
                    bands != meta.count
                    or height != meta.height
                    or width != meta.width
                ):
                    raise RasterReadError(
                        "Read dimensions do not match validated metadata.",
                        code="DIMENSION_MISMATCH",
                    )

                return data, meta

        except (ValidationError, RasterReadError):
            raise
        except rasterio.RasterioError as exc:
            raise RasterReadError(
                f"Rasterio error reading {path_obj}: {exc}",
                code="RASTER_IO_ERROR",
            ) from exc
        except Exception as exc:
            raise RasterReadError(
                f"Unexpected error reading raster: {exc}",
                code="UNEXPECTED_READ_ERROR",
            ) from exc
