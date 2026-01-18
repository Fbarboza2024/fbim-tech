FROM python:3.11-slim
WORKDIR /app

COPY ../core ./core
COPY kill_service.py .

RUN pip install docker filelock

CMD ["python", "kill_service.py"]
