
import uuid
from typing import Literal, Optional, Dict, Union

from pydantic import BaseModel, Field

from satquery.schemas.raster import RasterMetadataSchema


class ProcessingRecord(BaseModel):
    operation: str = Field(
        ...,
        description="Name of the geospatial operation performed",
    )
    parameters: Dict[str, Union[str, int, float, bool, None]] = Field(
        default_factory=dict,
        description="Parameters used during the operation",
    )


class AssetManifest(BaseModel):
    asset_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Stable unique asset identifier",
    )
    source_filename: str = Field(
        ...,
        description="Original descriptive filename",
    )
    media_type: Literal["geospatial_raster"] = "geospatial_raster"
    status: Literal["staged", "validated", "prepared"] = "staged"
    storage_key: str = Field(
        ...,
        description="Relative storage identifier",
    )
    metadata: Optional[RasterMetadataSchema] = None
    processing: tuple[ProcessingRecord, ...] = Field(
        default_factory=tuple,
        description="Processing history",
    )
