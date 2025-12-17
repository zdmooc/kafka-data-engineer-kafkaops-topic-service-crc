FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# Build deps for confluent-kafka (librdkafka comes from wheel for manylinux)
RUN pip install -U pip

COPY pyproject.toml /app/pyproject.toml
COPY app /app/app
COPY kafkaops_cli /app/kafkaops_cli

RUN pip install -e ".[dev]" &&     useradd -m appuser

USER appuser

ENV APP_PORT=8088
EXPOSE 8088

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8088"]
