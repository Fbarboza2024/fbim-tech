FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY lab_service.py .
RUN pip install filelock
CMD ["python", "lab_service.py"]
