FROM python:3.11-slim

RUN apt-get update && apt-get install -y bash git curl jq && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY environment /environment
COPY tests /tests
COPY solution /solution

RUN chmod +x /environment/setup.sh /environment/bin/gws /tests/test.sh /solution/solve.sh
