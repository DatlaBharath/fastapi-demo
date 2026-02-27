FROM python:3.12-slim

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory inside the container
WORKDIR /app

# Copy application code
COPY app.py .

# Change ownership of application files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Install FastAPI and Uvicorn (ASGI server)
RUN pip install --no-cache-dir fastapi uvicorn requests

# Expose the port service-b runs on
EXPOSE 5001

# Run the FastAPI app with Uvicorn on port 5001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]