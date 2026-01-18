FROM python:3.11-slim
WORKDIR /app

COPY ../core ./core
COPY rollback_service.py .

RUN pip install docker filelock

CMD ["python", "rollback_service.py"]
