import os

import pytest
from fastapi.testclient import TestClient

os.environ["KAFKA_BOOTSTRAP_SERVERS"] = "localhost:9092"  # not used for unit test

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_endpoint_exists():
    r = client.get("/metrics")
    assert r.status_code == 200
