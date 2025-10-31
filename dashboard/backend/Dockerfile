# Start from an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy ONLY the requirements file first (for better caching)
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
# This copies the 'app' folder (with main.py) into the container's /app/app
COPY ./app ./app

# Command to run the application
# Tells uvicorn to look for the 'app' variable inside the 'main' module located in the 'app' directory
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]