uv init
uv add uvicorn fastapi
uv add --dev ruff
source .venv/Scripts/activate

Instala apenas as dependencias do projeto:

uv pip install -r pyproject.toml

Instala todas as dependencias junto com as de desenvolvimento:

uv pip install -r pyproject.toml --group dev
uv pip install -r pyproject.toml --all-extras

Recompila serviço com o docker-compose.yaml:

docker-compose up -d --no-deps --build server

1ª Etapa:

```
FROM python:3.13-bullseye

RUN pip install uv

COPY . .

RUN uv venv
RUN uv pip install -r pyproject.toml

ENTRYPOINT ["uv", "run", "python", "-m", "server.main"]
```

Resultado:
cache-server latest 469569cc3ba8 6 minutes ago 1.55GB

2ª Etapa:

```
FROM python:3.13-bullseye

RUN pip install uv==0.6.12

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY server ./server

RUN uv venv
RUN uv pip install -r pyproject.toml

ENTRYPOINT ["uv", "run", "python", "-m", "server.main"]
```

Resultado:
cache-server latest 8cc3957ed31e About a minute ago 1.49GB

3ª Etapa:

```
FROM python:3.13-bullseye

RUN pip install uv==0.6.12

ENV UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv
RUN . .venv/bin/activate
RUN uv sync --no-dev --no-install-project && rm -rf $UV_CACHE_DIR

COPY server ./server

ENTRYPOINT ["uv", "run", "python", "-m", "server.main"]
```

Resultado:
cache-server latest b2b967b7aa6c About a minute ago 1.48GB

4ª Etapa:

```
FROM python:3.13-bullseye AS builder

RUN pip install uv==0.6.12
ENV UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv
RUN . .venv/bin/activate
RUN uv sync --no-dev --no-install-project && rm -rf $UV_CACHE_DIR

FROM python:3.13-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY server ./server

ENTRYPOINT ["python", "-m", "server.main"]
```

Resultado:
cache-server latest 2f0cd07c240f 25 seconds ago 196MB

5ª Etapa:

```
# Stage 1: the builder image, used to build the virtual environment
FROM python:3.13-bullseye AS builder

RUN pip install uv==0.6.12

ENV UV_CACHE_DIR=/tmp/uv_cache

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv
RUN . .venv/bin/activate
RUN --mount=type=cache,target=$UV_CACHE_DIR uv sync --no-dev --no-install-project

# Stage 2: the runtime image, used to just run the code provided its virtual environment
FROM python:3.13-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY server ./server

ENTRYPOINT ["python", "-m", "server.main"]
```

Resultado:
cache-server latest b387d7065641 2 hours ago 196MB
