
from pathlib import Path
from typing import Any, Dict, List

import yaml

from satquery.core.exceptions import ConfigurationError


SUPPORTED_TASKS = {"vqa", "captioning", "grounding"}


def load_model_registry(path: Path | str) -> List[Dict[str, Any]]:
    """Load and validate specialist model definitions from YAML."""
    path_obj = Path(path)

    if not path_obj.exists():
        raise ConfigurationError(
            f"Model registry not found: {path_obj}",
            code="REGISTRY_NOT_FOUND",
        )

    try:
        with path_obj.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except Exception as exc:
        raise ConfigurationError(
            f"Unable to parse model registry: {exc}",
            code="REGISTRY_PARSE_ERROR",
        ) from exc

    if not isinstance(data, dict) or "models" not in data:
        raise ConfigurationError(
            "Registry must contain a 'models' key.",
            code="INVALID_REGISTRY_STRUCTURE",
        )

    models = data["models"]

    if not isinstance(models, list) or not models:
        raise ConfigurationError(
            "Registry must contain a non-empty models list.",
            code="EMPTY_REGISTRY",
        )

    for entry in models:
        if not isinstance(entry, dict):
            raise ConfigurationError(
                "Each model entry must be a dictionary.",
                code="INVALID_MODEL_ENTRY",
            )

        task = entry.get("task")
        if task not in SUPPORTED_TASKS:
            raise ConfigurationError(
                f"Unsupported model task: {task}",
                code="UNSUPPORTED_TASK",
            )

        if not isinstance(entry.get("model_id"), str) or not entry["model_id"].strip():
            raise ConfigurationError(
                "Each model requires a non-empty model_id.",
                code="MISSING_MODEL_ID",
            )

        if "enabled" in entry and not isinstance(entry["enabled"], bool):
            raise ConfigurationError(
                "Model 'enabled' must be a boolean.",
                code="INVALID_ENABLED_VALUE",
            )

    return models
