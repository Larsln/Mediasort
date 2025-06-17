# Verwende ein offizielles Python-Image als Basis
FROM python:3.10-slim

# Installiere exiftool und andere notwendige Pakete
RUN apt-get update && apt-get install -y \
    exiftool \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die Anforderungen (requirements.txt) und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung in das Image
COPY . .