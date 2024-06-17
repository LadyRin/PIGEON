FROM python:3.12.4-bookworm

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y libsasl2-dev python-dev-is-python3 libldap2-dev libssl-dev ldap-utils && \
    apt-get clean && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["sh", "/app/django.sh"]
