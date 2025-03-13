FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project
RUN uv run huggingface-cli download intfloat/multilingual-e5-small model.safetensors config.json tokenizer.json tokenizer_config.json

#

FROM python:3.12-slim-bookworm AS production

COPY --from=builder /app /app
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY . .
