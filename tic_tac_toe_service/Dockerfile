### BUILDER ###
FROM python:3.12-alpine AS python-base

RUN apk add --no-cache \
    build-base \
    curl \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3-dev

# Install poetry w/ pip
RUN pip install --upgrade pip \
    && pip install poetry

# Disable poetry virtual envs
RUN poetry config virtualenvs.create false

# install dependencies using poetry
FROM python-base as poetry

# Copy lock and toml
COPY poetry.lock pyproject.toml ./

# install all packages
RUN poetry install --no-interaction --no-ansi --no-dev

### RUNTIME ###
FROM python:3.12-alpine AS runtime
WORKDIR /app

COPY --from=poetry /usr/local /usr/local
COPY . .

EXPOSE 5000

# Run the app
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "run:app"]
