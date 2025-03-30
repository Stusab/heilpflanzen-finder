# Basis-Image mit Python
FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Lokale Dateien ins Image kopieren
COPY . .

# NLTK vorbereiten (z. B. punkt-Tokenizer)
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import nltk; nltk.download('punkt')"

# Exponiere Port für Streamlit
EXPOSE 8501

# Startbefehl
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
