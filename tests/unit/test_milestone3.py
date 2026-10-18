
import pytest
from PIL import Image

from satquery.core.exceptions import ConfigurationError
from satquery.models.registry import load_model_registry
from satquery.schemas.model_results import ModelResult
from satquery.models.adapters.vqa import VQAAdapter
from satquery.models.adapters.captioning import CaptioningAdapter
from satquery.models.loader import load_single_image_model
from satquery.application.single_image_service import SingleImageService


def test_load_model_registry_success():
    models = load_model_registry("configs/model_registry.yaml")
    assert len(models) >= 2
    assert models[0]["task"] == "vqa"
    assert models[1]["task"] == "captioning"


def test_load_model_registry_not_found():
    with pytest.raises(ConfigurationError) as exc:
        load_model_registry("configs/nonexistent.yaml")
    assert exc.value.code == "REGISTRY_NOT_FOUND"


def test_model_result_schema():
    result = ModelResult(
        task="vqa",
        model_id="test-model",
        answer="building",
        input_asset_ids=("asset-123",),
        confidence=0.95,
    )
    assert result.task == "vqa"
    assert result.confidence == 0.95


def test_vqa_adapter_mock(tmp_path):
    image_path = tmp_path / "test.jpg"
    Image.new("RGB", (10, 10)).save(image_path, format="JPEG")

    def mock_pipeline(image, question):
        assert image.mode == "RGB"
        assert question == "What is this?"
        return [{"answer": "forest", "score": 0.88}]

    adapter = VQAAdapter(mock_pipeline, "test-vqa")
    result = adapter.predict(
        image_path,
        question="What is this?",
        asset_id="asset-1",
    )

    assert result.answer == "forest"
    assert result.confidence == pytest.approx(0.88)
    assert result.task == "vqa"
    assert result.input_asset_ids == ("asset-1",)


def test_vqa_requires_question(tmp_path):
    image_path = tmp_path / "test.jpg"
    Image.new("RGB", (10, 10)).save(image_path, format="JPEG")

    adapter = VQAAdapter(
        lambda image, question: [{"answer": "forest"}],
        "test-vqa",
    )

    from satquery.core.exceptions import ValidationError

    with pytest.raises(ValidationError):
        adapter.predict(image_path, question="  ")


def test_captioning_adapter_mock(tmp_path):
    image_path = tmp_path / "test.jpg"
    Image.new("RGB", (10, 10)).save(image_path, format="JPEG")

    adapter = CaptioningAdapter(
        lambda image: [{"generated_text": "A satellite image of a city."}],
        "test-captioner",
    )
    result = adapter.predict(image_path, asset_id="asset-caption")

    assert result.task == "captioning"
    assert result.answer == "A satellite image of a city."
    assert result.input_asset_ids == ("asset-caption",)


def test_loader_with_mock_pipeline():
    adapter = load_single_image_model(
        {
            "task": "vqa",
            "model_id": "test-vqa",
            "enabled": True,
        },
        mock_pipeline=lambda image, question: [{"answer": "water"}],
    )
    assert isinstance(adapter, VQAAdapter)


def test_loader_rejects_disabled_model():
    with pytest.raises(ConfigurationError) as exc:
        load_single_image_model(
            {
                "task": "vqa",
                "model_id": "test-vqa",
                "enabled": False,
            },
            mock_pipeline=lambda image, question: [],
        )
    assert exc.value.code == "MODEL_DISABLED"


def test_loader_without_pipeline_is_explicit():
    with pytest.raises(ConfigurationError) as exc:
        load_single_image_model(
            {
                "task": "vqa",
                "model_id": "test-vqa",
                "enabled": True,
            }
        )
    assert exc.value.code == "WEIGHTS_NOT_LOADED"


def test_single_image_service_vqa(tmp_path):
    # Use a real TIFF so the existing file validator sees valid image data.
    image_path = tmp_path / "test.tif"
    Image.new("RGB", (10, 10)).save(image_path, format="TIFF")

    adapter = VQAAdapter(
        lambda image, question: [{"answer": "water", "score": 0.92}],
        "test-vqa",
    )
    service = SingleImageService({"vqa": adapter})

    result = service.execute(
        image_path,
        "asset-99",
        "vqa",
        question="What body of water?",
    )

    assert result.answer == "water"
    assert result.task == "vqa"
    assert result.input_asset_ids == ("asset-99",)


def test_single_image_service_rejects_unknown_task(tmp_path):
    service = SingleImageService({})

    with pytest.raises(ConfigurationError) as exc:
        service.execute(
            tmp_path / "unused.tif",
            "asset-1",
            "unknown-task",
        )

    assert exc.value.code == "UNSUPPORTED_TASK"
