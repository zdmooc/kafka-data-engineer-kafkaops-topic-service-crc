from __future__ import annotations

import time
from contextlib import contextmanager

from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

HTTP_REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
HTTP_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "path"])
KAFKA_ADMIN_CALLS = Histogram("kafka_admin_call_duration_seconds", "Kafka admin call latency", ["op"])


@contextmanager
def observe_http(method: str, path: str):
    start = time.time()
    status = "500"
    try:
        yield lambda s: s
        status = "200"
    finally:
        dur = time.time() - start
        HTTP_LATENCY.labels(method=method, path=path).observe(dur)
        HTTP_REQUESTS.labels(method=method, path=path, status=status).inc()


def metrics_endpoint() -> Response:
    return Response(generate_latest(), media_type="text/plain")
