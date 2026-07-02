FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml README.md ./
COPY src ./src
COPY dashboard ./dashboard
RUN pip install --no-cache-dir -e ".[api]"
CMD ["uvicorn", "dashboard.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
