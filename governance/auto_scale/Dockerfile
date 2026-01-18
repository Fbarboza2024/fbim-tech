FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY scale_service.py .
RUN pip install filelock
CMD ["python", "scale_service.py"]
