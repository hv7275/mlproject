FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# build-essential is needed when a package falls back to building from source.
# libgomp1 provides OpenMP support used by packages such as scikit-learn and XGBoost.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy package metadata first so dependency installation can be cached.
COPY requirements.txt setup.py ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir gunicorn -r requirements.txt

COPY . .

RUN mkdir -p Database \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} application:application"]
