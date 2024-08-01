
FROM python:3.11.4

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY src/ ./src/
COPY run.py .
COPY .env .env

ENV PYTHONPATH=/usr/src/app/src

# 애플리케이션에서 사용되는 포트를 노출
EXPOSE 8000

CMD ["poetry", "run", "python", "run.py"]
