# 🛰️ SatQuery AI: Geospatial Intelligence SaaS Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

SatQuery AI is a geospatial intelligence project designed to help users
analyze satellite raster imagery and explore environmental information
through a natural-language interface.

The project is being developed with a modular Python architecture, with
FastAPI for backend APIs, Streamlit for the user interface, and geospatial
libraries for raster processing and validation.

## System Architecture

```text
User
 |
 v
Streamlit Interface
 |
 v
FastAPI Backend
 |
 v
Query Processing and Validation
 |
 v
Geospatial Engine
 |
 v
Raster Data and Analytical Results
```

## Core Capabilities

- Satellite raster input and geospatial metadata validation.
- NDVI calculation for vegetation analysis.
- API endpoints for health checks and spatial queries.
- Automated tests using pytest.
- Continuous integration using GitHub Actions.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Geospatial processing | Rasterio, NumPy |
| Machine learning | PyTorch, Transformers (planned or integrated as implemented) |
| Testing | pytest |
| CI | GitHub Actions |

## Project Structure

```text
satquery-ai/
├── satquery/
│   ├── api/
│   └── core/
├── tests/
├── .github/
│   └── workflows/
├── README.md
└── pyproject.toml
```

The exact structure may evolve as implementation progresses.

## Setup

Clone the repository and enter the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd satquery-ai
```

Create and activate a virtual environment, then install dependencies
according to the project's package configuration.

```bash
python -m venv .venv
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the project if its package configuration supports editable installs:

```bash
pip install -e .
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Run the API

Use the actual FastAPI application module configured in the repository.
For example, if the application is exposed as `satquery.api.main:app`:

```bash
uvicorn satquery.api.main:app --reload
```

## Development Status

This README documents the intended project architecture and development
workflow. Features, model integrations, performance metrics, and deployment
capabilities should be described as completed only after they have been
implemented and verified.

## License

See the LICENSE file if one is present in this repository.
