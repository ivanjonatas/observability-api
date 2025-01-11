# app/routes/__init__.py
from .crypto import router as crypto_router
from .monitoring import router as monitoring_router

__all__ = ["crypto_router", "monitoring_router"]