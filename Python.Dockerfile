FROM python:latest

ADD app/* /app/
ADD .env /
ADD poetry.lock /
ADD pyproject.toml /

EXPOSE 8000

ENV PYTHONPATH = /

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install
ENTRYPOINT poetry run uvicorn app.main:app --host 0.0.0.0
