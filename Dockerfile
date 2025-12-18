FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv sync
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose the port
EXPOSE 10000

# Environment variables
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# ⭐ KLJUČNA IZMJENA: Koristi uv run umjesto direktnog python
CMD ["uv", "run", "python", "main.py"]
