FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py config.py extensions.py ./
COPY wsgi.py ./
COPY detection ./detection
COPY models ./models
COPY routes ./routes
COPY scraper ./scraper
COPY static ./static
COPY templates ./templates
RUN useradd --system --create-home --home-dir /app slopguard \
    && mkdir -p /app/instance \
    && chown -R slopguard:slopguard /app
USER slopguard

EXPOSE 8000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "--timeout", "60", "wsgi:app"]
