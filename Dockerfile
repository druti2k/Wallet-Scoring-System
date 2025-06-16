# Dockerfile for FastAPI backend
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src
COPY src ./src
COPY src/api ./src/api
COPY src/blockchain ./src/blockchain
COPY src/langchain_tools ./src/langchain_tools
COPY src/ml ./src/ml
COPY src/utils ./src/utils

# Expose port
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
