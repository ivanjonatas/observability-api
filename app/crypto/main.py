from fastapi import FastAPI
from app.crypto.routes import crypto, routes_monitoring

app = FastAPI()

# Registra os routers
app.include_router(crypto.router, prefix="/crypto", tags=["Crypto"])
app.include_router(routes_monitoring.router, prefix="/monitoring", tags=["Monitoring"])

# O FastAPI automaticamente agrupa rotas com base no prefixo e tags.
