
from typing import Any, Dict

from satquery.core.exceptions import ConfigurationError
from satquery.models.adapters.captioning import CaptioningAdapter
from satquery.models.adapters.vqa import VQAAdapter


def load_single_image_model(
    spec: Dict[str, Any],
    mock_pipeline=None,
):
    """Build an adapter. Real pretrained-weight loading is not enabled yet."""
    if not spec.get("enabled", True):
        raise ConfigurationError(
            f"Model '{spec.get('model_id')}' is disabled.",
            code="MODEL_DISABLED",
        )

    task = spec.get("task")
    model_id = spec.get("model_id")

    if not model_id:
        raise ConfigurationError(
            "Model specification is missing model_id.",
            code="MISSING_MODEL_ID",
        )

    if task not in {"vqa", "captioning"}:
        raise ConfigurationError(
            f"Unsupported single-image task: {task}",
            code="UNSUPPORTED_TASK",
        )

    if mock_pipeline is None:
        raise ConfigurationError(
            "Real model loading is not implemented in this milestone.",
            code="WEIGHTS_NOT_LOADED",
        )

    if task == "vqa":
        return VQAAdapter(mock_pipeline, model_id)

    return CaptioningAdapter(mock_pipeline, model_id)
