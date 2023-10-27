FROM python:3.11.12-alpine AS base

LABEL maintainer="Jhunu Fernandes jhunu.fernandes@gmail.com"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache build-base libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt uvicorn && \
    apk del build-base libffi-dev openssl-dev

FROM base AS final

COPY ./src /app/src

EXPOSE 80

ENV APP_SPEC_FILE="app_spec.py"

ENTRYPOINT ["uvicorn", "app.src.run:app"]

CMD ["--host", "0.0.0.0", "--port", "80"]
