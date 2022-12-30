## Build Environment
FROM python:3.10 AS env

# Poetry version...also used as version to plugin
ENV POETRY_VERSION=1.3.1
ENV POETRY_HOME=/opt/poetry

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add to path
ENV PATH=/opt/poetry/bin:$PATH

# Install poetry deps and the current project
# Copy poetry config
COPY poetry.lock pyproject.toml ./
# Also copy source etc
COPY ./src README.md ./
RUN /opt/poetry/bin/poetry install -n --no-dev

# Command is to run the app
CMD ["/opt/poetry/bin/poetry", "run", "jotbackend"]