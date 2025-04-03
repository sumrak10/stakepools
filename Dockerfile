###########
# BUILDER #
###########
FROM python:3.12 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_DEV=1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

###########
## IMAGE ##
###########
FROM python:3.12-slim

WORKDIR /home/appuser/app

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /home/appuser/app

RUN mkdir -p /logs && \
    chown appuser: /logs

COPY --from=builder /usr/local /usr/local

COPY . /home/appuser/app

RUN sed -i 's/\r$//' /home/appuser/app/start_app.sh && \
    chmod +x /home/appuser/app/start_app.sh

USER appuser

EXPOSE 8560

ENTRYPOINT ["./start_app.sh"]
