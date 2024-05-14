FROM python:3.10-buster

ARG CODEARTIFACT_AUTH_TOKEN=""
ARG POETRY_VERSION=1.3.2

WORKDIR /app/

# Install poetry
# Don't create venv in container
ENV POETRY_HOME=/opt/poetry POETRY_VERSION=${POETRY_VERSION} POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

# Poetry uses these files to install dependencies
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

# Auth poetry to install from codeartifact repository
# Use specified poetry version
# Only install production dependencies
# Remove auth from poetry after installing everything
RUN  poetry config http-basic.drift aws ${CODEARTIFACT_AUTH_TOKEN} \
        && poetry install --no-root --no-dev --no-interaction --no-ansi \
        && poetry config --unset http-basic.drift

COPY . /app/

# Corresponds to `containerPort` in k8s config
EXPOSE 8080

ENTRYPOINT ["gunicorn", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8080", "app.main:app"]
