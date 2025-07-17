# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13.5-alpine

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /sailmanager

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY ./sailmanager /sailmanager

RUN chown -R appuser:appuser /sailmanager

RUN mkdir /sailmanager/logging -p && chown appuser:appuser /sailmanager/logging

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Set the user to appuser *after* permissions are set
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SailingManager.wsgi"]
