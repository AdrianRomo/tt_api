# We use Python 3.8
FROM python:3.8

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN pip install --upgrade pip

# Set the workdir as /app
WORKDIR /app

# Copy the requirements.txt
COPY ./tt_api/src/requirements.txt /app/src/requirements.txt

# Install python programmer-defined dependencies
RUN pip install --no-cache-dir -r src/requirements.txt

# Install gunicorn to run the application in production
RUN pip install gunicorn
# Copy the entire source for the application
COPY ./tt_api /app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --worker-class=gthread --timeout 0 src.app:app