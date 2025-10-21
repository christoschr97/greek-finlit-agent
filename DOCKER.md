# Docker Guide

Super simple Docker setup using `uv`.

## Quick Start

```bash
# Build and run
docker-compose up

# Run in background
docker-compose up -d

# Stop
docker-compose down
```

Access at: **http://localhost:8501**

## That's It!

The Dockerfile:
- Installs `uv`
- Copies your project
- Runs `uv sync` (just like locally)
- Starts Streamlit

No complexity, just works! 🚀
