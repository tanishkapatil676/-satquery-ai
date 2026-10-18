import rasterio
import math
from satquery.core.exceptions import ValidationError, RasterReadError
from satquery.core.config import settings
from satquery.schemas.raster import RasterMetadataSchema, RasterBoundsSchema

class RasterValidator:
    @staticmethod
    def validate_and_extract(file_path: str) -> RasterMetadataSchema:
        try:
            with rasterio.open(file_path) as src:
                width = src.width
                height = src.height
                count = src.count

                if width <= 0 or height <= 0 or count <= 0:
                    raise ValidationError("Raster dimensions and band count must be positive integers.", code="INVALID_DIMENSIONS")

                total_pixels = width * height
                if total_pixels > settings.satquery_max_raster_pixels:
                    raise ValidationError(f"Raster pixel count {total_pixels} exceeds limit {settings.satquery_max_raster_pixels}.", code="PIXEL_LIMIT_EXCEEDED")

                if src.crs is None:
                    raise ValidationError("Raster file lacks a Coordinate Reference System (CRS).", code="MISSING_CRS")

                bounds = src.bounds
                for val in [bounds.left, bounds.bottom, bounds.right, bounds.top]:
                    if not math.isfinite(val):
                        raise ValidationError("Raster bounds contain non-finite values.", code="INVALID_BOUNDS")

                return RasterMetadataSchema(
                    driver=src.driver,
                    width=width,
                    height=height,
                    count=count,
                    crs=str(src.crs),
                    bounds=RasterBoundsSchema(left=bounds.left, bottom=bounds.bottom, right=bounds.right, top=bounds.top),
                    res=list(src.res),
                    nodata=src.nodata,
                    dtypes=list(src.dtypes)
                )
        except rasterio.RasterioError as e:
            raise RasterReadError(f"Failed to parse raster file: {str(e)}", code="RASTER_PARSE_ERROR")
