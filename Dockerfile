FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY promises.csv .
COPY startup.txt .

# Create reports directory
RUN mkdir -p reports

# Expose port
EXPOSE 8050

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "4", "--timeout", "120", "src.app:server"]
