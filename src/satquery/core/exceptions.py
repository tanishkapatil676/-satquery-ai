class SatQueryError(Exception):
    """Base exception for SatQuery AI."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(SatQueryError):
    """Raised when file or raster validation fails."""

    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message, code)


class RasterReadError(SatQueryError):
    """Raised when Rasterio fails to open or read a raster."""

    def __init__(self, message: str, code: str = "RASTER_READ_ERROR"):
        super().__init__(message, code)
