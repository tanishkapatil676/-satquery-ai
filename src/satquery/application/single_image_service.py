
from pathlib import Path
from typing import Dict, Optional

from satquery.core.exceptions import ConfigurationError
from satquery.models.base import SingleImageModel
from satquery.schemas.model_results import ModelResult
from satquery.validation.file_validator import FileValidator


class SingleImageService:
    """Coordinate validation and execution of a single-image adapter."""

    def __init__(self, adapters: Dict[str, SingleImageModel]):
        self.adapters = adapters

    def execute(
        self,
        staged_path: Path,
        asset_id: str,
        task: str,
        question: Optional[str] = None,
    ) -> ModelResult:
        if task not in self.adapters:
            raise ConfigurationError(
                f"No adapter loaded for task '{task}'.",
                code="UNSUPPORTED_TASK",
            )

        # Retain the project's existing upload/file validation contract.
        FileValidator.validate(str(staged_path))

        adapter = self.adapters[task]
        return adapter.predict(
            image_path=Path(staged_path),
            question=question,
            asset_id=asset_id,
        )
