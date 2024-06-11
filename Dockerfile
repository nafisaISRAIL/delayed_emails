FROM python:3.11.3-slim-bullseye

EXPOSE 8000

ENV \
    # allow for log messages to be immediately dumped to the stream instead of being buffered
    PYTHONUNBUFFERED=1 \
    # prevent python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # choose version
    POETRY_VERSION=1.4.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # do not ask any interactive questions
    POETRY_NO_INTERACTION=1 \
    # User for app launch
    USER="app"

WORKDIR /app

ENV PATH="${PATH}:${POETRY_HOME}/bin" \
    PYTHONPATH="${PYTHONPATH}:/app"

COPY poetry.lock pyproject.toml ./

RUN \
	# install libs
    apt-get update \
    && build_deps='curl' \
    && runtime_deps='' \
     && apt-get install -y ${build_deps} ${runtime_deps} \
    # install poetry
    && curl -sSL https://install.python-poetry.org | python3 -  \
    && poetry --version \
    # install dependencies
    && poetry install --only main --no-root --no-cache \
    # purge
    && pip cache purge \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts} \
    && apt-get purge -y --auto-remove ${build_deps} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # create user
    && useradd --shell /bin/bash ${USER}

COPY delayed_email/ delayed_email/

RUN  \
	# install root package
    poetry install --only-root \
    && poetry cache clear . --all -n

USER $USER

CMD poetry run python -m delayed_email.api
