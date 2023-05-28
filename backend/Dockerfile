FROM python:3.7-slim
WORKDIR /app
COPY ./backend/requirements.txt /
RUN apt-get upgrade -y
RUN apt-get install -y libpq-dev gcc netcat
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]