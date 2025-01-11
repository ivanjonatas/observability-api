from fastapi import APIRouter
from prometheus_client import generate_latest
from fastapi.responses import PlainTextResponse
from app.crypto.routes.monitor import monitor_instance

router = APIRouter()

@router.get("/health")
@monitor_instance.track
def health_check():
    return {"status": "ok"}

@router.get("/metrics")
@monitor_instance.track
def metrics():
    """
    Endpoint para expor métricas no formato Prometheus.
    """
    return PlainTextResponse(generate_latest())