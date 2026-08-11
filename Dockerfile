FROM python:3.10.4-bullseye

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN pip install pip==26.0.1 setuptools==82.0.1 --upgrade --hash=sha256:c4037d8a277c89b320abe636d59f91e6d0922d08a05b60e85e53b296613346d8 --hash=sha256:7d872682c5d01cfde07da7bccc7b65469d3dca203318515ada1de5eda35efbf9

RUN python -m pip install --no-cache-dir scanapi==2.13.2

COPY . /app

WORKDIR /app

CMD ["scanapi"]
