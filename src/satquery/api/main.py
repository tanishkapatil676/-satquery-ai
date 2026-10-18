from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from satquery.api.v1.router import router as api_v1_router

def create_app() -> FastAPI:
    app = FastAPI(title="SatQuery AI API", version="1.0.0", description="ISRO SIH 2026")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(api_v1_router)
    return app

app = create_app()
