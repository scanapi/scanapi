FROM python:3.10.4-bullseye@sha256:86862fd2ad17902cc3a95b7effd257dfd043151f05d280170bdd6ff34f7bc78b

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN python -m pip install --no-cache-dir \
    pip==26.1.2 --hash=sha256:382ff9f685ee3bc25864f820aa50505825f10f5458ffff07e30a6d96e5715cab \
    setuptools==82.0.1 --hash=sha256:a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb

RUN python -m pip install --no-cache-dir \
    scanapi==2.13.2 --hash=sha256:6d31091d43521f4fc3ead545bdf72af6e18ce19e682bab57733212213bd74a8b

COPY . /app

WORKDIR /app

CMD ["scanapi"]
