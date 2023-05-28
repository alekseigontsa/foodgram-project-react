FROM python:3.7-slim
WORKDIR /app
COPY ./backend/requirements.txt /
RUN pip3 install --upgrade pip
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gcc \
        libc6-dev \
        libpq-dev \
        sox \
        ffmpeg \
        libcairo2 \
        libcairo2-dev \
        texlive-full \
    && pip3 install -r /requirements.txt --no-cache-dir \
    && apt-get purge --assume-yes --auto-remove \
        gcc \
        libc6-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
# RUN python3 manage.py migrate
# RUN python3 manage.py collectstatic --no-input
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]