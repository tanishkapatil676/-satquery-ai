
from pathlib import Path
from typing import Optional

from satquery.core.exceptions import SatQueryError
from satquery.models.base import SingleImageModel
from satquery.models.image_preprocessor import ImagePreprocessor
from satquery.schemas.model_results import ModelResult


class CaptioningAdapter(SingleImageModel):
    """Adapter for an image-captioning pipeline."""

    def __init__(self, pipeline_fn, model_id: str):
        self.pipeline_fn = pipeline_fn
        self.model_id = model_id

    def predict(
        self,
        image_path: Path,
        question: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> ModelResult:
        pil_image = ImagePreprocessor.prepare_ordinary_image(image_path)

        try:
            output = self.pipeline_fn(pil_image)

            if isinstance(output, list):
                if not output:
                    raise ValueError("The captioning pipeline returned an empty list.")
                output = output[0]

            if isinstance(output, dict):
                caption = output.get(
                    "generated_text",
                    output.get("caption", str(output)),
                )
            else:
                caption = str(output)

            return ModelResult(
                task="captioning",
                model_id=self.model_id,
                answer=str(caption),
                input_asset_ids=(asset_id or "unknown",),
                confidence=None,
                evidence={},
                warnings=(),
            )
        except SatQueryError:
            raise
        except Exception as exc:
            raise SatQueryError(
                f"Captioning inference failed: {exc}",
                code="INFERENCE_ERROR",
            ) from exc
