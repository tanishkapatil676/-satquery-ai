import rasterio
import numpy as np
from typing import Dict, Any


class GeospatialEngine:
    """Utilities for inspecting rasters and calculating NDVI."""

    @staticmethod
    def inspect_raster(file_path: str) -> Dict[str, Any]:
        """Inspect raster metadata without loading the entire raster array."""
        with rasterio.open(file_path) as src:
            bounds = src.bounds

            return {
                "driver": src.driver,
                "width": src.width,
                "height": src.height,
                "count": src.count,
                "crs": str(src.crs) if src.crs else None,
                "bounds": {
                    "left": bounds.left,
                    "bottom": bounds.bottom,
                    "right": bounds.right,
                    "top": bounds.top,
                },
                "res": src.res,
                "nodata": src.nodata,
            }

    @staticmethod
    def calculate_ndvi(
        red_band: np.ndarray,
        nir_band: np.ndarray,
    ) -> np.ndarray:
        """Calculate NDVI = (NIR - Red) / (NIR + Red)."""
        red = np.asarray(red_band, dtype=np.float32)
        nir = np.asarray(nir_band, dtype=np.float32)

        if red.shape != nir.shape:
            raise ValueError("Red and NIR bands must have matching shapes.")

        denominator = nir + red
        ndvi = np.zeros_like(denominator, dtype=np.float32)

        np.divide(
            nir - red,
            denominator,
            out=ndvi,
            where=np.isfinite(denominator) & (denominator != 0),
        )

        # Mark invalid input pixels as NaN rather than treating them as data.
        invalid = ~np.isfinite(red) | ~np.isfinite(nir)
        ndvi[invalid] = np.nan

        return ndvi
