#!/usr/bin/env python3
"""Entry point for local development - loads .env, runs uvicorn."""

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("FASTAPI_PORT", 8000))
    host = os.environ.get("FASTAPI_HOST", "0.0.0.0")
    uvicorn.run("api.main:app", host=host, port=port, reload=True)
