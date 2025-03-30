import requests
from bs4 import BeautifulSoup

# URL der Zielseite
url = "https://www.meine-gesundheit.de/medizin/heilpflanzen/birkenblaetter"

# Seite mit Requests abrufen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

# BeautifulSoup zum Parsen des HTML-Inhalts verwenden
soup = BeautifulSoup(response.text, "html.parser")

# Testen, ob "Anwendungsgebiete" existiert
anwendungsgebiete_section = soup.find("h2", text="Anwendungsgebiete")

if anwendungsgebiete_section:
    ul = anwendungsgebiete_section.find_next("ul")  # Finde die nächste <ul>-Liste
    if ul:
        symptome = [li.get_text(strip=True) for li in ul.find_all("li")]
        print("✅ Gefundene Anwendungsgebiete:", symptome)
    else:
        print("❌ Keine Liste nach 'Anwendungsgebiete' gefunden.")
else:
    print("❌ 'Anwendungsgebiete' nicht gefunden.")

