FROM python:3.7-slim
WORKDIR /app
COPY ./requirements.txt /
RUN pip3 install --upgrade pip
# RUN apt-get update \
#     && apt-get install --assume-yes --no-install-recommends \
#         gcc \
#         libc6-dev \
#         libpq-dev \
#         libcairo2 \
#         libcairo2-dev \
#     && pip3 install -r /requirements.txt --no-cache-dir \
#     && apt-get purge --assume-yes --auto-remove \
#         gcc \
#         libc6-dev \
#         libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . ./
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]