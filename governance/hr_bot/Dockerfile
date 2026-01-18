FROM python:3.11-slim
WORKDIR /app
COPY ../core ./core
COPY hr_service.py .
RUN pip install filelock
CMD ["python", "hr_service.py"]
