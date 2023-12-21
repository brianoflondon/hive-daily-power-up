FROM python:3.11

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR  /app/

# needed for pymssql to install in 3.11
RUN apt update && apt install -y freetds-dev && rm -rf /var/lib/apt/lists/*

RUN poetry install --only main

COPY ./src /app/

ENV PATH="/home/hive_daily_power_up/app/.venv/bin:${PATH}"

ENTRYPOINT [ "python", "./main.py" ]