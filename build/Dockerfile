
FROM python:3.11-alpine AS base

LABEL maintainer="Jhunu Fernandes jhunu.fernandes@gmail.com"

ENV SRC_PATH=/app

COPY build/requirements.txt ${SRC_PATH}/requirements.txt

WORKDIR ${SRC_PATH}

RUN apk add --no-cache build-base libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt uvicorn && \
    apk del build-base libffi-dev openssl-dev

FROM base AS final

COPY /src ${SRC_PATH}

EXPOSE 80

ENTRYPOINT ["uvicorn"]

CMD ["run:app", "--host", "0.0.0.0", "--port", "80"]
