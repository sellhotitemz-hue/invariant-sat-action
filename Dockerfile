FROM python:3.11-slim

LABEL maintainer="Invariant SAT Platform <security@invariantsat.com>"
LABEL description="Zero-IP GitHub Action Container for Invariant SAT ZK Security Scanner"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    jq \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /github/workspace

COPY requirements.txt /app/requirements.txt
COPY enterprise_client.py /app/enterprise_client.py
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
