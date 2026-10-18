
from typing import Dict, Any

from satquery.core.exceptions import ValidationError
from satquery.schemas.raster import RasterMetadataSchema


class AlignmentValidator:
    @staticmethod
    def validate_spatial_alignment(
        meta_a: RasterMetadataSchema,
        meta_b: RasterMetadataSchema,
    ) -> Dict[str, Any]:
        """Check CRS, dimensions, resolution, and bounds."""

        if meta_a.crs != meta_b.crs:
            raise ValidationError(
                f"CRS mismatch: {meta_a.crs} versus {meta_b.crs}.",
                code="CRS_MISMATCH",
            )

        if (
            meta_a.width != meta_b.width
            or meta_a.height != meta_b.height
        ):
            raise ValidationError(
                "Raster dimensions do not match.",
                code="DIMENSION_MISMATCH",
            )

        if len(meta_a.res) != len(meta_b.res) or any(
            abs(float(a) - float(b)) > 1e-9
            for a, b in zip(meta_a.res, meta_b.res)
        ):
            raise ValidationError(
                "Raster resolutions do not match.",
                code="RESOLUTION_MISMATCH",
            )

        bounds_a = meta_a.bounds
        bounds_b = meta_b.bounds
        tolerance = 1e-6

        if any(
            abs(a - b) > tolerance
            for a, b in [
                (bounds_a.left, bounds_b.left),
                (bounds_a.bottom, bounds_b.bottom),
                (bounds_a.right, bounds_b.right),
                (bounds_a.top, bounds_b.top),
            ]
        ):
            raise ValidationError(
                "Raster bounding extents do not match.",
                code="EXTENT_MISMATCH",
            )

        return {
            "alignment_status": "grid_compatible",
            "crs": meta_a.crs,
            "resolution": meta_a.res,
            "dimensions": [meta_a.width, meta_a.height],
        }
