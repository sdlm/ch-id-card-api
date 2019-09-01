FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-runtime

WORKDIR /webapp

RUN pip install poetry
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry config settings.virtualenvs.create false && \
    poetry install --no-dev --no-ansi --no-interaction
