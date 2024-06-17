
FROM python:3.11.4

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY src/ ./src/
COPY run.py .
COPY .env .env

ENV PYTHONPATH=/usr/src/app/src

CMD ["poetry", "run", "python", "run.py"]
