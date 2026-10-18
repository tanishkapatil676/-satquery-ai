
from typing import Any, Dict, Literal, Optional, Tuple

from pydantic import BaseModel, Field


class ModelResult(BaseModel):
    """Standard output contract for a specialist image model."""

    task: Literal["vqa", "captioning", "grounding"] = Field(
        ..., description="Specialist task type"
    )
    model_id: str = Field(
        ..., description="Identifier of the model used"
    )
    answer: str = Field(
        ..., description="Generated answer or caption"
    )
    input_asset_ids: Tuple[str, ...] = Field(
        ..., description="IDs of the input assets"
    )
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0,
        description="Optional confidence score"
    )
    evidence: Dict[str, Any] = Field(default_factory=dict)
    warnings: Tuple[str, ...] = Field(default_factory=tuple)
