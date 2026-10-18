
from pathlib import Path

from PIL import Image

from satquery.core.exceptions import ValidationError


class ImagePreprocessor:
    """Prepare ordinary images for model inference."""

    @staticmethod
    def prepare_ordinary_image(image_path: Path) -> Image.Image:
        """Open a JPEG/PNG or other supported image and convert it to RGB."""
        try:
            with Image.open(image_path) as image:
                image.load()
                return image.convert("RGB")
        except Exception as exc:
            raise ValidationError(
                f"Failed to load ordinary image: {exc}",
                code="IMAGE_LOAD_ERROR",
            ) from exc
