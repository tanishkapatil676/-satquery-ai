from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, model_validator

TaskType = Literal["vqa", "captioning", "change_detection", "optical_sar_fusion", "spatial_evidence"]

class QueryApiRequest(BaseModel):
    task: TaskType
    asset_ids: List[str] = Field(..., min_length=1, max_length=2)
    question: Optional[str] = None
    options: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_request_by_task(self) -> "QueryApiRequest":
        if self.task in ["vqa", "captioning"] and len(self.asset_ids) != 1:
            raise ValueError(f"Task '{self.task}' requires exactly 1 asset ID.")
        
        if self.task in ["change_detection", "optical_sar_fusion"] and len(self.asset_ids) != 2:
            raise ValueError(f"Task '{self.task}' requires exactly 2 asset IDs.")
            
        if self.task in ["change_detection", "optical_sar_fusion"] and self.asset_ids[0] == self.asset_ids[1]:
            raise ValueError("Asset IDs must be distinct.")
            
        if self.task == "vqa" and (not self.question or not self.question.strip()):
            raise ValueError("Task 'vqa' requires a non-empty question.")
            
        return self

class QueryApiResponse(BaseModel):
    status: Literal["success", "failed", "rejected"]
    task: TaskType
    answer: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    asset_ids: List[str]
    evidence: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)

class AssetMetadataResponse(BaseModel):
    asset_id: str
    filename: str
    modality: str
    crs: str
    dimensions: List[int]
    bounds: List[float]
    band_count: int
    created_at: str
