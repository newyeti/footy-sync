# Use an official Python runtime as a parent image
FROM python:3.10.13-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /code
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
COPY ./scripts/dockerenv.sh /app/scripts/env.sh
COPY ./scripts/start_app.sh /app/scripts/start.sh

ENTRYPOINT [ "./scripts/start.sh" ] 

# Run app.py when the container launches
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
