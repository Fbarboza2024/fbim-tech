FROM python:3.11-slim
WORKDIR /app

COPY ../core ./core
COPY chaos_service.py .

RUN pip install docker filelock

CMD ["python", "chaos_service.py"]
