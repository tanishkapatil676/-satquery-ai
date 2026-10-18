
from typing import Optional, Dict, Any

from satquery.core.exceptions import ValidationError
from satquery.schemas.raster import RasterMetadataSchema


class TemporalValidator:
    @staticmethod
    def validate_bitemporal_compatibility(
        meta_a: RasterMetadataSchema,
        meta_b: RasterMetadataSchema,
        timestamp_a: Optional[str] = None,
        timestamp_b: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validate spatial compatibility and acquisition timestamps."""

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
                "Bi-temporal raster dimensions do not match.",
                code="DIMENSION_MISMATCH",
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
                "Bi-temporal spatial bounds do not align.",
                code="BOUNDS_MISMATCH",
            )

        if not timestamp_a or not timestamp_b:
            timestamp_status = "missing_timestamps"
        else:
            if timestamp_a == timestamp_b:
                raise ValidationError(
                    "Acquisition timestamps must be distinct.",
                    code="IDENTICAL_TIMESTAMPS",
                )
            timestamp_status = "distinct_timestamps"

        return {
            "status": "compatible",
            "temporal_status": timestamp_status,
            "timestamp_a": timestamp_a,
            "timestamp_b": timestamp_b,
            "crs": meta_a.crs,
        }
