FROM python:3.10.4-bullseye

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN pip install pip setuptools --upgrade

RUN python -m pip install --no-cache-dir scanapi==2.13.2

COPY . /app

WORKDIR /app

CMD ["scanapi"]
