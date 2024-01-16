FROM python:3.11.2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1

WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.in-project false

COPY ./FastAPI/pyproject.toml ./pyproject.toml
COPY ./FastAPI/poetry.lock ./poetry.lock
RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
