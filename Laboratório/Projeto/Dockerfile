FROM python:3.11-slim

WORKDIR /app
COPY backend/ /app/
RUN pip install flask pymongo redis

CMD ["python", "app.py"]
