# 1. Start with a lightweight Python base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. Tell Docker we are listening on port 8000
EXPOSE 8000

# 7. The command to run your app
# Note: --host 0.0.0.0 is crucial for Docker to accept outside connections
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]