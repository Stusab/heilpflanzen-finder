import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Lade die JSON-Datei mit fehlenden Symptomen
with open("heilpflanzen_ohne_symptome.json", encoding="utf-8") as f:
    eintraege = json.load(f)

# Starte Headless-Browser
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

ergebnisse = []

for eintrag in eintraege:
    name = eintrag["name"]
    url = eintrag["url"]
    symptome = []

    try:
        driver.get(url)
        time.sleep(2)

        # XPath: finde das <li>, das "Anwendungsgebiete" enthält
        elemente = driver.find_elements(By.XPATH, '//li[contains(text(), "Anwendungsgebiete")]')

        for el in elemente:
            symptome.append(el.text.strip())

        # Versuche, nachfolgende <li>-Elemente ebenfalls zu bekommen
        folge_elemente = driver.find_elements(By.XPATH, '//li[contains(text(), "Anwendungsgebiete")]/following-sibling::li[position() <= 2]')
        for el in folge_elemente:
            symptome.append(el.text.strip())

        symptome = [s for s in symptome if s]
        if not symptome:
            symptome = ["Keine Angabe"]

    except Exception as e:
        symptome = [f"Fehler: {str(e)}"]

    ergebnisse.append({
        "name": name,
        "url": url,
        "symptome": symptome
    })

driver.quit()

# Ergebnisse speichern
with open("heilpflanzen_symptome_selenium.json", "w", encoding="utf-8") as f:
    json.dump(ergebnisse, f, ensure_ascii=False, indent=2)

print("✅ Fertig! Ergebnisse in heilpflanzen_symptome_selenium.json gespeichert.")
