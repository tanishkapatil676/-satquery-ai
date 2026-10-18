from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RasterInspectRequest(BaseModel):
    file_path: str = Field(
        ...,
        description="Path to a raster inside the configured upload directory",
    )


class RasterBounds(BaseModel):
    left: float
    bottom: float
    right: float
    top: float


class RasterInspectResponse(BaseModel):
    driver: str
    width: int
    height: int
    count: int
    crs: Optional[str] = None
    bounds: RasterBounds
    res: List[float]
    nodata: Optional[Any] = None


class SpatialQueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Natural-language geospatial query",
    )
    raster_path: str = Field(
        ...,
        description="Path to a raster inside the configured upload directory",
    )
    bbox: Optional[List[float]] = Field(
        None,
        description="Optional bounding box [xmin, ymin, xmax, ymax]",
    )


class SpatialQueryResponse(BaseModel):
    status: str
    query_received: str
    analysis_results: Dict[str, Any]
