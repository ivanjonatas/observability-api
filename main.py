from fastapi import FastAPI, HTTPException
import requests
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import time

# Inicialização do Tracer e Métricas
resource = Resource.create(attributes={"service.name": "crypto-api"})
trace.set_tracer_provider(TracerProvider(resource=resource))
meter_provider = MeterProvider(metric_readers=[PrometheusMetricReader()])
tracer = trace.get_tracer(__name__)
meter = meter_provider.get_meter("crypto-meter")

# Inicializar o Span Exporter para OTLP (pode ser integrado com Jaeger, Tempo ou OTEL)
span_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter))

# Métricas Prometheus
REQUEST_COUNT = Counter("api_requests_total", "Total de requisições para a API")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latência das requisições para a API")

# Criação da API
app = FastAPI()

# Instrumentação automática do FastAPI e Requests
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

@app.get("/crypto")
def get_crypto_data():
    start_time = time.time()
    with tracer.start_as_current_span("get_crypto_data") as span:
        try:
            REQUEST_COUNT.inc()
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
            response.raise_for_status()
            data = response.json()
            
            # Adicionar atributos ao span (dados importantes para tracing)
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("api.endpoint", "/crypto")
            span.set_attribute("crypto.currency", "Bitcoin")

            latency = time.time() - start_time
            REQUEST_LATENCY.observe(latency)

            return {
                "Bitcoin (USD)": data["bpi"]["USD"]["rate"],
                "Bitcoin (EUR)": data["bpi"]["EUR"]["rate"]
            }
        except requests.RequestException as e:
            span.record_exception(e)
            raise HTTPException(status_code=500, detail="Erro ao buscar dados de criptomoeda")

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest())

@app.get("/health")
def health_check():
    return {"status": "ok"}
