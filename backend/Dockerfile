FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn
COPY backend /app/backend
COPY frontend /app/frontend
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

