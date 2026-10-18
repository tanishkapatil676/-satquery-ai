
from pathlib import Path
from typing import Optional

from satquery.core.exceptions import SatQueryError, ValidationError
from satquery.models.base import SingleImageModel
from satquery.models.image_preprocessor import ImagePreprocessor
from satquery.schemas.model_results import ModelResult


class VQAAdapter(SingleImageModel):
    """Adapter for a visual question-answering pipeline."""

    def __init__(self, pipeline_fn, model_id: str):
        self.pipeline_fn = pipeline_fn
        self.model_id = model_id

    def predict(
        self,
        image_path: Path,
        question: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> ModelResult:
        if not question or not question.strip():
            raise ValidationError(
                "VQA requires a non-empty question.",
                code="MISSING_QUESTION",
            )

        pil_image = ImagePreprocessor.prepare_ordinary_image(image_path)

        try:
            output = self.pipeline_fn(
                image=pil_image,
                question=question,
            )

            if isinstance(output, list):
                if not output:
                    raise ValueError("The VQA pipeline returned an empty list.")
                output = output[0]

            if isinstance(output, dict):
                answer = output.get("answer", output.get("generated_text", str(output)))
                score = output.get("score")
            else:
                answer = str(output)
                score = None

            confidence = float(score) if score is not None else None

            return ModelResult(
                task="vqa",
                model_id=self.model_id,
                answer=str(answer),
                input_asset_ids=(asset_id or "unknown",),
                confidence=confidence,
                evidence={"question": question},
                warnings=(),
            )
        except SatQueryError:
            raise
        except Exception as exc:
            raise SatQueryError(
                f"VQA inference failed: {exc}",
                code="INFERENCE_ERROR",
            ) from exc
