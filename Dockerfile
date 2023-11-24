FROM python:3.10.12-alpine

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

RUN chmod +x /app/django.sh

# entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]