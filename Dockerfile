# Minimal Dockerfile using uv (mirrors local development)
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy everything
COPY . .

# Install dependencies with uv
RUN uv sync

# Expose Streamlit port
EXPOSE 8501

# Run with uv
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]