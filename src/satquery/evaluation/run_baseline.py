import json
import time
import platform
from pathlib import Path

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from satquery.evaluation.metrics import exact_match, token_f1


def run_evaluation(
    samples_file="artifacts/evaluation/eval_samples.json",
    model_id="Salesforce/blip-image-captioning-base",
    output_dir="artifacts/evaluation",
    max_new_tokens=40,
):
    """
    Evaluate actual BLIP-generated captions against supplied references.

    samples_file must contain a JSON list such as:
    [
      {"image": "data/images/image1.jpg",
       "reference": "urban residential area with roads"}
    ]

    Image paths may be absolute or relative to the project directory.
    """
    project_dir = Path.cwd()
    samples_path = Path(samples_file)
    if not samples_path.is_absolute():
        samples_path = project_dir / samples_path

    if not samples_path.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {samples_path}\n"
            "Create the JSON file with real image paths and reference captions."
        )

    samples = json.loads(samples_path.read_text(encoding="utf-8"))
    if not isinstance(samples, list) or not samples:
        raise ValueError("Evaluation JSON must contain a non-empty list.")

    for index, sample in enumerate(samples):
        if not isinstance(sample, dict) or not sample.get("image") or not sample.get("reference"):
            raise ValueError(
                f"Sample {index} must contain 'image' and 'reference' fields."
            )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=== SatQuery AI: Real Baseline Evaluation ===")
    print(f"Model: {model_id}")
    print(f"Device: {device}")
    print(f"PyTorch: {torch.__version__}")
    print(f"Platform: {platform.platform()}")
    print(f"Examples: {len(samples)}")

    processor = BlipProcessor.from_pretrained(model_id)
    model = BlipForConditionalGeneration.from_pretrained(model_id)
    model.to(device)
    model.eval()

    details = []
    elapsed_inference = 0.0

    for index, sample in enumerate(samples):
        image_path = Path(sample["image"])
        if not image_path.is_absolute():
            image_path = project_dir / image_path

        if not image_path.is_file():
            raise FileNotFoundError(
                f"Image for sample {index} does not exist: {image_path}"
            )

        with Image.open(image_path) as source:
            image = source.convert("RGB")

        inputs = processor(images=image, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        start = time.perf_counter()
        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
            )
        elapsed = time.perf_counter() - start
        elapsed_inference += elapsed

        prediction = processor.decode(
            generated_ids[0],
            skip_special_tokens=True,
        ).strip()
        reference = sample["reference"].strip()

        details.append({
            "image": str(image_path),
            "reference": reference,
            "prediction": prediction,
            "exact_match": exact_match(prediction, reference),
            "token_f1": token_f1(prediction, reference),
            "inference_seconds": elapsed,
        })

        print(f"[{index + 1}/{len(samples)}] {prediction}")

    count = len(details)
    summary = {
        "model_id": model_id,
        "evaluation_type": "real_model_inference",
        "evaluated_examples": count,
        "mean_exact_match": sum(x["exact_match"] for x in details) / count,
        "mean_token_f1": sum(x["token_f1"] for x in details) / count,
        "total_inference_seconds": elapsed_inference,
        "mean_inference_seconds": elapsed_inference / count,
        "device": str(device),
        "pytorch_version": torch.__version__,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    report_file = output_path / "evaluation_report.json"
    report_file.write_text(
        json.dumps({"summary": summary, "details": details}, indent=2),
        encoding="utf-8",
    )

    print("\nEvaluation completed.")
    print(f"Report: {report_file}")
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    run_evaluation()
