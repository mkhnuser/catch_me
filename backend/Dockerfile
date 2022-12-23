FROM python:3.11-alpine AS base
WORKDIR /app
COPY [^tests]* .
RUN ["python", "-m", "pip", "install", "-U", "pip"]
RUN ["python", "-m", "pip", "install", "-r", "requirements.txt"]

FROM base AS testing
COPY tests .
CMD ["python", "-m", "pytest", "--durations=5", "--durations-min=0.1"]

FROM base AS production
CMD [ \
    "gunicorn", "main:create_app", \
     "--access-logfile", "-", \
     "--bind", "0.0.0.0:8080", \
     "--worker-class", "aiohttp.GunicornWebWorker" \
]
