# Official Python image as base
FROM python:3.12-slim

# stop .pyc generation
ENV PYTHONDONTWRITEBYTECODE=1
# real-time terminal output
ENV PYTHONUNBUFFERED=1 

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
