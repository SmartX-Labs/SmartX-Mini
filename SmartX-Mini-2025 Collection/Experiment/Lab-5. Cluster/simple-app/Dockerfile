FROM python:3.9-alpine

WORKDIR /app

COPY app.py .
RUN pip install --no-cache-dir flask
CMD ["python", "app.py"]