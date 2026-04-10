FROM python:3.10.4-bullseye@sha256:86862fd2ad17902cc3a95b7effd257dfd043151f05d280170bdd6ff34f7bc78b

LABEL maintainer="github.com/camilamaia"

ENV PATH="~/.local/bin:${PATH}"

RUN python -m pip install --no-cache-dir pip==26.0.1 \
    --hash=sha256:bdb1b08f4274833d62c1aa29e20907365a2ceb950410df15fc9521bad440122b \
    setuptools==82.0.1 \
    --hash=sha256:a59e362652f08dcd477c78bb6e7bd9d80a7995bc73ce773050228a348ce2e5bb

RUN python -m pip install --no-cache-dir scanapi==2.12.0 \
    --hash=sha256:5aa0e644c2037965c4c0c1db884bf4fc02078acb51c065700785de25557b5399

COPY . /app

WORKDIR /app

CMD ["scanapi"]
