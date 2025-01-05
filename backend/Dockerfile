# Build stage
FROM python:3.12 AS builder

WORKDIR /app

# Install poetry
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv .venv/

# Copy application code
COPY . .

# Install system dependencies
RUN apt-get update -y && \
    apt-get install libpq5 -y && \
    apt-get clean

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
