FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the local 'app' directory into the container's '/app' directory
COPY app/ .

# Now main.py and log_analyzer.py are both directly in /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
