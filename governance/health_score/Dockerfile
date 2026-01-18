FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY health_service.py .
RUN pip install filelock
CMD ["python", "health_service.py"]
