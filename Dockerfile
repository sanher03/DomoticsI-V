FROM node:22-alpine AS frontend

WORKDIR /frontend
COPY server_domotics/package.json server_domotics/package-lock.json ./
RUN npm ci

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/server_domotics

WORKDIR /app/server_domotics

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server_domotics/ /app/server_domotics/
COPY iot_devices/ /app/iot_devices/
COPY --from=frontend /frontend/node_modules/bootstrap/dist/css/bootstrap.min.css /app/server_domotics/static/vendor/bootstrap.min.css
COPY --from=frontend /frontend/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js /app/server_domotics/static/vendor/bootstrap.bundle.min.js

EXPOSE 8000
