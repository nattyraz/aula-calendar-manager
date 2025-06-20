FROM python:3.11-slim

# M?tadonn?es
LABEL maintainer="nattyraz@example.com"
LABEL description="Aula Calendar Manager - Gestionnaire de calendrier scolaire"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Dossier de travail
WORKDIR /app

# Installation des d?pendances syst?me
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des d?pendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app/ ./app/
COPY run.py .

# Cr?ation des dossiers n?cessaires
RUN mkdir -p logs data

# Utilisateur non-root pour la s?curit?
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Exposition du port
EXPOSE 8000

# Point d'entr?e
CMD ["python", "run.py"]