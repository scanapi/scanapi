FROM python:3.7

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN pip install pip setuptools --upgrade

RUN pip install scanapi

COPY . /app

WORKDIR /app

CMD ["scanapi"]
