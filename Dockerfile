FROM --platform=linux/amd64 python:3.10-buster as prepare

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN python -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config --local virtualenvs.in-project false && \
    poetry export -f requirements.txt -o requirements.txt

FROM --platform=linux/amd64 python:3.10-buster as builder

WORKDIR /app

COPY --from=prepare /app/requirements.txt /app/requirements.txt

RUN python -m pip install -r requirements.txt

FROM --platform=linux/amd64 python:3.10-slim-buster as runner

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/fastapi /usr/local/bin/uvicorn /usr/local/bin/
COPY ./src/data/ /app/src/data/
COPY ./src/model/ /app/src/model/
COPY ./src/type/ /app/src/type/
COPY ./src/util/ /app/src/util/
COPY ./src/*.py /app/src/
COPY ./src/web/dist /app/src/web/dist

EXPOSE 8000

CMD ["fastapi", "run", "src/app.py", "--host", "0.0.0.0", "--port", "8000"]