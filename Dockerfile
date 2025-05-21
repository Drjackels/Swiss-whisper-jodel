##FROM python:3.9-slim

##WORKDIR /app

# Copy and install dependencies
##COPY requirements.txt .
##RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
##COPY . .

# Expose the port the app will run on
##ENV PORT 8080
##EXPOSE 8080

# Run the application using gunicorn
##CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies (for example, for ffmpeg and GPU libraries)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port that Flask listens on
EXPOSE 8080

# Command to run the application (using gunicorn for production)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]
