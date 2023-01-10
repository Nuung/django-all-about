ARG PYTHON_VERSION=3.8-slim-buster
ARG APP_HOME=/app

FROM python:${PYTHON_VERSION}


# update & install 
RUN apt-get update && apt-get install -y \
  wget \
  gnupg2 \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

WORKDIR ${APP_HOME}

# 다양한 running scripts가 필요하게 될 수 있다.
COPY ./scripts /scripts
ENV PATH ${PATH}:/scripts
