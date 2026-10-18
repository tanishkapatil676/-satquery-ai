from fastapi import APIRouter
from satquery.api.v1.endpoints import health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
