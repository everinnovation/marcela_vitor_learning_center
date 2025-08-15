FROM python:3.10.5

EXPOSE 8000
WORKDIR /app

# Install gettext for translations
RUN apt-get update && apt-get install -y gettext

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD ./platform /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--reload", "app.wsgi:application"]