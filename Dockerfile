# Use official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Set working directory
WORKDIR /app

# Copy dependencies files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
