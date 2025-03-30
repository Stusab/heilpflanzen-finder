# 🌿 Heilpflanzen Finder

Finde passende Heilpflanzen basierend auf Symptomen – mithilfe von Textsimilarität und maschinellem Lernen. Die App analysiert typische Anwendungsgebiete von Heilpflanzen und gibt Vorschläge auf Basis ähnlicher Beschwerden.

---

## 🧠 Funktionsweise
- Die Datenbasis besteht aus strukturierten Heilpflanzen-Informationen inkl. Symptomen.
- Mittels **TF-IDF Vektorisierung** und **Cosine Similarity** wird die Ähnlichkeit zwischen Benutzereingabe und Pflanzendaten berechnet.
- Die App gibt die **Top-N Heilpflanzen** zur Eingabe aus.

---

## 🚀 Projektstruktur

```bash
heilpflanzen-finder/
├── app.py                          # Streamlit App
├── symptom_model.py               # Modelllogik für Textsimilarität
├── heilpflanzen_symptome_ready.csv # Finalisierte Datenbasis
├── requirements.txt               # Python-Abhängigkeiten
├── dockerfile                     # Containerisierung
├── extract_selenium.py            # (Optional) Webscraping-Logik
├── test_bs4.py                    # (Optional) BeautifulSoup Test
├── scrapy.cfg                     # (Optional) Scrapy-Konfiguration
```

---

## 🧪 Beispielverwendung

```text
Eingabe:
"Blähungen und Völlegefühl"

Ausgabe:
1. Pfefferminze (Mentha piperita)
2. Rosmarin (Rosmarinus officinalis)
3. Benediktenkraut (Cnicus benedictus)
```

---

## 🛠️ Lokales Setup

```bash
# Repository klonen
git clone https://github.com/Stusab/heilpflanzen-finder.git
cd heilpflanzen-finder

# Virtuelle Umgebung erstellen (optional)
python -m venv .venv
source .venv/bin/activate  # oder .venv\Scripts\activate auf Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
streamlit run app.py
```

---

## 🐳 Docker-Nutzung (optional)

```bash
# Image bauen
docker build -t heilpflanzen-app .

# Container starten
docker run -p 8501:8501 heilpflanzen-app
```

Dann im Browser auf `http://localhost:8501` zugreifen.

---

## 👤 Autorin
**Sabrina Studer**  
ZHAW / Modul: Model Deployment & Maintenance (FS25)


## 📄 Lizenz
Dieses Projekt ist Teil eines Hochschulmoduls und nicht für den kommerziellen Einsatz bestimmt.

