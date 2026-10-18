from typing import Any, Dict

import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification


class ModelLoader:
    """Lazy-loading image classification model wrapper."""

    def __init__(
        self,
        model_name_or_path: str = "google/vit-base-patch16-224",
    ):
        self.model_name = model_name_or_path
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.processor = None
        self.model = None

    def load_model(self):
        """Load the processor and model only when first needed."""
        if self.model is None:
            self.processor = AutoImageProcessor.from_pretrained(
                self.model_name
            )
            self.model = AutoModelForImageClassification.from_pretrained(
                self.model_name
            )
            self.model.to(self.device)
            self.model.eval()

    def predict(self, image: Any) -> Dict[str, Any]:
        """Classify a PIL image or another supported image input."""
        self.load_model()

        inputs = self.processor(
            images=image,
            return_tensors="pt",
        )
        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(outputs.logits, dim=-1)
        predicted_id = int(probabilities.argmax(dim=-1).item())

        return {
            "predicted_class_id": predicted_id,
            "predicted_label": self.model.config.id2label.get(
                predicted_id, str(predicted_id)
            ),
            "confidence": float(probabilities[0, predicted_id].item()),
            "device_used": str(self.device),
        }
