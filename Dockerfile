
FROM python:3.11-alpine AS base

LABEL maintainer="Jhunu Fernandes jhunu.fernandes@gmail.com"

ENV SRC_PATH=/app

COPY pyproject.toml ${SRC_PATH}/pyproject.toml

RUN mkdir -p ${SRC_PATH}/volume

VOLUME ${SRC_PATH}/volume

WORKDIR ${SRC_PATH}

RUN apk add --no-cache build-base libffi-dev openssl-dev && \
    python -m pip install --no-cache-dir .[stage] && \
    apk del build-base libffi-dev openssl-dev

FROM base AS final

COPY /src ${SRC_PATH}

EXPOSE 80

ENTRYPOINT ["uvicorn"]

CMD ["run:app", "--host", "0.0.0.0", "--port", "80"]
