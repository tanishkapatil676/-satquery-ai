
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from satquery.schemas.model_results import ModelResult


class SingleImageModel(ABC):
    """Interface implemented by single-image specialist models."""

    @abstractmethod
    def predict(
        self,
        image_path: Path,
        question: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> ModelResult:
        """Run a specialist prediction on one image."""
        raise NotImplementedError
