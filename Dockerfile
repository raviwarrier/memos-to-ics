FROM python:3.12-slim

# Prevent Python from writing bytecode (.pyc) and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies using pinned wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

# Security Best Practice: Create a dedicated non-root user to run the app.
# Works out of the box for all environments — no configuration required.
RUN useradd -u 10001 -m appuser && \
    chown -R appuser:appuser /app
USER appuser

COPY app.py .

EXPOSE 5321

CMD ["gunicorn", "--bind", "0.0.0.0:5321", "--workers", "2", "app:app"]
