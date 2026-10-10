FROM python:3.12-slim

# Prevent Python from writing bytecode (.pyc) and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# Install dependencies with locked versions and create dedicated non-root user
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt && \
    useradd -u 10001 -m appuser && \
    chown -R appuser:appuser /app

USER appuser

COPY app.py .

EXPOSE 5321

CMD ["gunicorn", "--bind", "0.0.0.0:5321", "--workers", "2", "app:app"]
