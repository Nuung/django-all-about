ARG PYTHON_VERSION=3.8-slim-buster
ARG APP_HOME=/app

FROM python:${PYTHON_VERSION}

# update & install 
RUN apt-get update && apt-get install -y \
  wget \
  gnupg2 \
  procps \
  unzip \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# promtail install & run
RUN wget https://github.com/grafana/loki/releases/download/v2.2.1/promtail-linux-amd64.zip \
    && unzip promtail-linux-amd64.zip \
    && rm promtail-linux-amd64.zip

# Install dockerize to wait depedencies
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

WORKDIR ${APP_HOME}

# 다양한 running scripts가 필요하게 될 수 있다.
COPY ./scripts /scripts
ENV PATH ${PATH}:/scripts

COPY . /app

ENTRYPOINT ["docker-entrypoint.sh"]