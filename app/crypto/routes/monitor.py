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
            f"{request_metric_name}_total", f"Total de {description}"
        )
        self.latency_histogram = Histogram(
            f"{latency_metric_name}_latency_seconds",
            f"Latência de {description} (em segundos)"
        )

    def track(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Incrementa o contador de requisições
            self.request_counter.inc()
            start_time = time.time()  # Inicia o cronômetro
            try:
                # Executa a função decorada
                return func(*args, **kwargs)
            finally:
                # Observa a latência
                elapsed_time = time.time() - start_time
                self.latency_histogram.observe(elapsed_time)
        return wrapper

monitor_instance = Monitor("external_api_requests", "external_api", "requisições para API externa")