# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy application code
COPY app.py .

# Install FastAPI, Uvicorn, Requests, and Redis client
RUN pip install --no-cache-dir fastapi uvicorn requests redis

# Expose the port service-a runs on
EXPOSE 5000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]