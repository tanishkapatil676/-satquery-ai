from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RasterBoundsSchema(BaseModel):
    left: float
    bottom: float
    right: float
    top: float

class RasterMetadataSchema(BaseModel):
    driver: str
    width: int
    height: int
    count: int
    crs: Optional[str] = None
    bounds: RasterBoundsSchema
    res: List[float]
    nodata: Optional[Any] = None
    dtypes: List[str]
