FROM python:3.10.4-bullseye

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN pip install pip setuptools --upgrade

RUN pip install scanapi==2.7.0

COPY . /app

WORKDIR /app

CMD ["scanapi"]
