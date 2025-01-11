from prometheus_client import Counter, Histogram
from functools import wraps
import time

class Monitor:
    def __init__(self, request_metric_name, latency_metric_name, description=""):
        """
        Classe de monitoramento para contagem e medição de latência.

        :param request_metric_name: Nome do contador para requisições
        :param latency_metric_name: Nome do histograma para latência
        :param description: Descrição das métricas
        """
        self.request_counter = Counter(
            f"{request_metric_name}_total",
            f"Total de {description}",
            labelnames=["endpoint"]
        )
        self.latency_histogram = Histogram(
            f"{latency_metric_name}_latency_seconds",
            f"Latência de {description} (em segundos)",
            labelnames=["endpoint"]
        )

    def track(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            endpoint_name = func.__name__
            self.request_counter.labels(endpoint=endpoint_name).inc()
            start_time = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_time = time.time() - start_time
                self.latency_histogram.labels(endpoint=endpoint_name).observe(elapsed_time)
        return wrapper

monitor_instance = Monitor("external_api_requests", "external_api", "requisições para API externa")