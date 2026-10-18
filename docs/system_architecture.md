# System Architecture: SatQuery AI

## Overview

SatQuery AI is designed around a decoupled client-server architecture. The
frontend handles user interaction, the backend validates requests, and the
core processing layer performs geospatial operations and, when implemented,
machine-learning inference.

## Architecture

```text
+--------------------------------------+
|          Streamlit Frontend          |
|        src/satquery/frontend/        |
|  Uploads, queries, result display    |
+-------------------+------------------+
                    |
                    | HTTP / JSON / multipart
                    v
+--------------------------------------+
|           FastAPI Backend            |
|           src/satquery/api/          |
|  Request validation and API routes  |
+-------------------+------------------+
                    |
                    | Internal Python calls
                    v
+--------------------------------------+
|       Geospatial Processing Core     |
|           src/satquery/core/         |
| Raster validation and spatial logic |
+--------------------------------------+
```

## Main Components

### Frontend
The Streamlit frontend is intended to provide upload controls, natural-language
query input, and displays for analysis results.

### Backend
The FastAPI service is intended to expose health checks and validated endpoints
for raster inspection and geospatial queries.

### Processing Core
The processing layer is intended to isolate raster validation, coordinate
reference system handling, and geospatial analysis from API and UI code.

### Data Flow
1. The user submits an image or query through the frontend.
2. The backend validates the request and uploaded file.
3. The processing layer performs supported operations.
4. The backend returns a structured response.
5. The frontend displays the result.

## Implementation Status

This document describes the intended architecture. An endpoint, model, or
security control should be considered implemented only after its code and
behavior have been verified.
