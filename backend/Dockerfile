FROM python:3.7-slim
WORKDIR /app
COPY ./backend/requirements.txt /
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get purge --assume-yes --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install libcairo2-dev pkg-config python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]