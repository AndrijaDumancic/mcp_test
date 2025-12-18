FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 10000

ENV PORT=10000
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
