from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from app.database import engine
from app.core.config import settings

# Custom metrics
CUSTOMER_CREATED = Counter('customer_created_total', 'Total number of customers created')
CUSTOMER_UPDATED = Counter('customer_updated_total', 'Total number of customers updated')
CUSTOMER_DELETED = Counter('customer_deleted_total', 'Total number of customers deleted')


def setup_telemetry(app):
    # Set up metrics
    instrumentator = Instrumentator()

    # Instrument the app and expose metrics
    instrumentator.instrument(app).expose(app)

    # Set up tracing
    trace.set_tracer_provider(TracerProvider())
    otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(engine=engine)


def increment_customer_created():
    CUSTOMER_CREATED.inc()


def increment_customer_updated():
    CUSTOMER_UPDATED.inc()


def increment_customer_deleted():
    CUSTOMER_DELETED.inc()