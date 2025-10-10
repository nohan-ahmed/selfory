# Base image
FROM python:3.13-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Use system Python (no .venv)
ENV UV_SYSTEM_PYTHON=1
# Avoid hardlink issues on overlayfs
ENV UV_LINK_MODE=copy
# Compile bytecode for speed
ENV UV_COMPILE_BYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files for caching
COPY pyproject.toml uv.lock ./

# Install dependencies (system mode, no .venv)
RUN uv sync --locked

# Copy the rest of your app
COPY . .

# Expose Django/FastAPI port
EXPOSE 8000

# Default command (example: Django)
# CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
