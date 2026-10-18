import os
from pathlib import Path

from fastapi import FastAPI, HTTPException

from satquery.api.models import (
    RasterInspectRequest,
    RasterInspectResponse,
    SpatialQueryRequest,
    SpatialQueryResponse,
)
from satquery.core.geospatial import GeospatialEngine


app = FastAPI(
    title="SatQuery AI API",
    description="API for raster metadata inspection and geospatial queries.",
    version="2.0.0",
)


def resolve_upload_path(file_path: str) -> Path:
    """Resolve a raster path and restrict access to the upload directory."""
    upload_root = Path(
        os.environ.get("SATQUERY_UPLOAD_DIR", "./data/uploads")
    ).resolve()

    candidate = Path(file_path)
    if not candidate.is_absolute():
        candidate = upload_root / candidate

    resolved = candidate.resolve()

    try:
        resolved.relative_to(upload_root)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="File path must be inside the configured upload directory.",
        )

    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="Raster file not found.")

    return resolved


@app.get("/health", tags=["System"])
async def health_check():
    """Return basic API health information."""
    return {"status": "healthy", "service": "satquery-ai-backend"}


@app.post(
    "/api/v1/raster/inspect",
    response_model=RasterInspectResponse,
    tags=["Geospatial"],
)
async def inspect_raster_endpoint(payload: RasterInspectRequest):
    """Inspect metadata for an approved raster file."""
    raster_path = resolve_upload_path(payload.file_path)

    try:
        return GeospatialEngine.inspect_raster(str(raster_path))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Unable to inspect the supplied raster.",
        )


@app.post(
    "/api/v1/query",
    response_model=SpatialQueryResponse,
    tags=["Intelligence"],
)
async def spatial_query_endpoint(payload: SpatialQueryRequest):
    """Validate a query and confirm that its raster target exists."""
    resolve_upload_path(payload.raster_path)

    if payload.bbox is not None:
        if len(payload.bbox) != 4:
            raise HTTPException(
                status_code=422,
                detail="bbox must contain exactly four numbers.",
            )

        xmin, ymin, xmax, ymax = payload.bbox
        if xmin >= xmax or ymin >= ymax:
            raise HTTPException(
                status_code=422,
                detail="bbox minimum coordinates must be below maximum coordinates.",
            )

    # This endpoint is currently a validated placeholder.
    # Actual natural-language query routing is not implemented yet.
    return {
        "status": "accepted",
        "query_received": payload.query,
        "analysis_results": {
            "raster_target": payload.raster_path,
            "message": "Input validated; analysis pipeline is not implemented yet.",
        },
    }
