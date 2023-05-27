FROM python:3.9-slim
WORKDIR /app
COPY /backend/requirements.txt /
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input 