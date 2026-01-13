FROM python:3.13-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev || uv sync --no-dev

COPY . .

EXPOSE 10000

ENV PORT=10000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
