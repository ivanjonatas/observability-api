from fastapi import FastAPI
from volume_linux.volume_service import VolumeService
from volume_linux.metrics import registrar_coletor, coletar_metricas
from fastapi.responses import Response

app = FastAPI()

# Endpoint principal para listar volumes
@app.get("/volumes")
def listar_volumes():
    volumes = VolumeService.listar_volumes()
    return {"volumes": volumes}

# Endpoint para Prometheus
@app.get("/metrics")
def metrics():
    """Retorna métricas no formato Prometheus."""
    registrar_coletor()  # Atualiza as métricas
    return Response(content=coletar_metricas(), media_type="text/plain")

# Inicializa coletores de métricas no Prometheus
registrar_coletor()
