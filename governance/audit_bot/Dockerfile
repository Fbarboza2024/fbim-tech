FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY audit_service.py .
RUN pip install filelock
CMD ["python", "audit_service.py"]
