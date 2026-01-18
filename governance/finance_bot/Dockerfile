FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY finance_service.py .
RUN pip install filelock
CMD ["python", "finance_service.py"]
