FROM python:3.8.2-slim-buster as base
FROM base as builder

ADD requirements.txt /
# minnow requirements
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    automake \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libpq-dev \
    libffi-dev \
    gcc \
    libssl-dev

RUN pip3 install -r requirements.txt 
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get purge -y \
    libxml2-dev   \
    libxslt-dev   \
    zlib1g-dev    \
    libffi-dev    \
    gcc           \
    libssl-dev
RUN apt-get -y autoremove

# minnow code
ENV POSTGRES_HOST "tbot_postgres"
COPY . /usr/src/app

WORKDIR /usr/src/app

ENTRYPOINT [ "/usr/src/app/entrypoints/entrypoint.sh" ]
