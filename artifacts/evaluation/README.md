# Evaluation Artifacts: SatQuery AI

## Overview
This directory stores evaluation reports for pretrained and domain-adapted
SatQuery AI models.

## Metrics
- **Exact Match (EM):** normalized prediction must exactly match the reference.
- **Token F1:** harmonic mean of token-overlap precision and recall.
- **Inference time:** elapsed time for each model generation call.

## Prepare evaluation data
Create `artifacts/evaluation/eval_samples.json` containing a non-empty list:

```json
[
  {
    "image": "data/evaluation/image1.jpg",
    "reference": "urban residential area with roads"
  }
]
```

Use real images and human-verified reference captions. Image paths are relative
to the project root unless absolute paths are supplied.

## Run
From the project root:

```bash
python src/satquery/evaluation/run_baseline.py
```

The script loads BLIP and generates predictions from the supplied images.
It writes `evaluation_report.json` into this directory.

## Limitations
The four-image synthetic smoke dataset is not a valid benchmark. Token F1 and
exact match are diagnostic metrics, not substitutes for domain-specific
remote-sensing evaluation. Do not report results from synthetic examples as
real-world model performance.
