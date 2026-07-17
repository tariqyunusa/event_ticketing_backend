FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY alembic.ini .
COPY ./alembic ./alembic

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}