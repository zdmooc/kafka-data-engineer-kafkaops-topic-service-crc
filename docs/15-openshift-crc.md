# OpenShift Local (CRC) deployment notes

## Why CRC
- Matches OpenShift operational patterns (Operators, Routes, image registry)
- Allows demo of support tasks in a realistic environment

## Kafka on OpenShift
Recommended approach for Kafka on OpenShift is via an operator.
In this repo we provide a Strimzi path (OperatorHub + Kafka CR).

## Networking
- Internal Kafka access via Strimzi bootstrap service
- External access is intentionally not enabled for CRC demo (simplify)

## Images
Topic-as-a-Service is built via OpenShift BuildConfig (binary build from repo folder).
