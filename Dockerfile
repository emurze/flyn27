FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update && apt-get -y install curl

WORKDIR /service

COPY README.md .
COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY src src

EXPOSE 8080

CMD bash -c "flask db upgrade head -d src/migrations && \
cd src && gunicorn 'app:create_app()' --bind 0.0.0.0:8080 --workers 4"