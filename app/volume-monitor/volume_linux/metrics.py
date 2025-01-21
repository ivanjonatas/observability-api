from prometheus_client import Gauge, generate_latest, CollectorRegistry
from volume_linux.volume_service import VolumeService

# Registro de métricas
registry = CollectorRegistry()
gauge_volume_percentual = Gauge("volume_percentual_usado", "Percentual de uso de cada volume", ["volume"], registry=registry)
gauge_volume_total = Gauge("volume_total_mb", "Tamanho total do volume (MB)", ["volume"], registry=registry)
gauge_volume_usado = Gauge("volume_usado_mb", "Espaço usado no volume (MB)", ["volume"], registry=registry)
gauge_volume_livre = Gauge("volume_livre_mb", "Espaço livre no volume (MB)", ["volume"], registry=registry)

def bytes_para_mb(valor_em_bytes):
    """Converte bytes para megabytes (MB)."""
    return round(valor_em_bytes / (1024 ** 2), 2)

def registrar_coletor():
    """Registra métricas personalizadas."""
    volumes = VolumeService.listar_volumes()
    for volume in volumes:
        gauge_volume_percentual.labels(volume=volume["ponto_de_montagem"]).set(volume["percentual"])
        gauge_volume_total.labels(volume=volume["ponto_de_montagem"]).set(bytes_para_mb(volume["total"]))
        gauge_volume_usado.labels(volume=volume["ponto_de_montagem"]).set(bytes_para_mb(volume["usado"]))
        gauge_volume_livre.labels(volume=volume["ponto_de_montagem"]).set(bytes_para_mb(volume["livre"]))

def coletar_metricas():
    """Coleta as métricas no formato Prometheus."""
    registrar_coletor()
    return generate_latest(registry)
