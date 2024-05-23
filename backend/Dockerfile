FROM python:3.11

WORKDIR /app

RUN mkdir -p /app/logs

COPY ./pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./ ./

ENTRYPOINT ["/bin/sh", "-c", "uvicorn main:app --host 0.0.0.0"]