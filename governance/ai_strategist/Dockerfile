FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY strategist_service.py .
RUN pip install filelock
CMD ["python", "strategist_service.py"]
