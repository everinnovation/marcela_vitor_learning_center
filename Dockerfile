FROM python:3.10.5

EXPOSE 8000
WORKDIR /app

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD ./platform /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--reload", "app.wsgi:application"]