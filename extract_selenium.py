import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

# 🔐 MONGO_URI aus Umgebungsvariable lesen
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["heilpflanzen"]
collection = db["symptome"]

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

        elemente = driver.find_elements(By.XPATH, '//li[contains(text(), "Anwendungsgebiete")]')
        for el in elemente:
            symptome.append(el.text.strip())

        folge_elemente = driver.find_elements(By.XPATH, '//li[contains(text(), "Anwendungsgebiete")]/following-sibling::li[position() <= 2]')
        for el in folge_elemente:
            symptome.append(el.text.strip())

        symptome = [s for s in symptome if s]
        if not symptome:
            symptome = ["Keine Angabe"]

    except Exception as e:
        symptome = [f"Fehler: {str(e)}"]

    dokument = {
        "name": name,
        "url": url,
        "symptome": symptome
    }
    ergebnisse.append(dokument)
    collection.insert_one(dokument)

driver.quit()

print("✅ Fertig! Ergebnisse gespeichert in MongoDB.")
