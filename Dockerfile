# Base image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies and curl for uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install uv using pip
RUN pip install --upgrade pip \
 && pip install uv

# # Add uv to PATH
# ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy rest of the application
COPY . .

# Expose port for app (Django/FastAPI/etc.)
EXPOSE 8000

# Default command (you can customize)
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
