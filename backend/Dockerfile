FROM python:3.10.9-alpine AS base
WORKDIR /app
COPY . .
RUN ["python", "-m", "pip", "install", "-U", "pip"]
RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]
ENV RENDEZVOUS_TITLE_MIN_LENGTH=4
ENV RENDEZVOUS_TITLE_MAX_LENGTH=64
ENV RENDEZVOUS_DESCRIPTION_MIN_LENGTH=0
ENV RENDEZVOUS_DESCRIPTION_MAX_LENGTH=1024
ENV LATITUDE_MIN_VALUE=-90
ENV LATITUDE_MAX_VALUE=90
ENV LONGITUDE_MIN_VALUE=-180
ENV LONGITUDE_MAX_VALUE=180
ENV DB_CLOSE_TIMEOUT=1

FROM base AS testing
ENV DATABASE_URL=postgresql+asyncpg://testing:testing@database:5432/testing
CMD ["python", "-m", "pytest", "--durations=5", "--durations-min=0.1"]

FROM base AS production
ENV DATABASE_URL=postgresql+asyncpg://production:production@database:5432/production
CMD [ \
    "gunicorn", "main:create_app", \
     "--access-logfile", "-", \
     "--bind", "0.0.0.0:8080", \
     "--worker-class", "aiohttp.GunicornWebWorker" \
]
