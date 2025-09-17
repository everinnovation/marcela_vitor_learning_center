FROM python:3.10.5

EXPOSE 8000
WORKDIR /usr/src/app

# Install gettext for translations and netcat for health checks
RUN apt-get update && apt-get install -y gettext netcat-openbsd

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# No need to copy files as they will be mounted as volumes

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]