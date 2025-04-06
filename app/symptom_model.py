import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 CSV laden
df = pd.read_csv("heilpflanzen_symptome_ready.csv", encoding="utf-8", sep=",", quotechar='"', on_bad_lines="skip")


# 🔹 Semantisches Modell laden
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

# 🔹 Symptome encodieren
symptom_texts = df["symptome"].astype(str).tolist()
symptom_vectors = model.encode(symptom_texts, show_progress_bar=True)

# 🔹 Funktion: Benutzertext → passende Pflanzen
def finde_passende_pflanzen(symptom_text, top_n=5):
    if not symptom_text.strip():
        return []

    input_vector = model.encode([symptom_text])
    ähnlichkeit = cosine_similarity(input_vector, symptom_vectors).flatten()

    if max(ähnlichkeit) == 0:
        return []

    top_indices = ähnlichkeit.argsort()[::-1][:top_n]

    ergebnisse = []
    for idx in top_indices:
        ergebnisse.append({
            "name": df.iloc[idx]["name"],
            "symptome": df.iloc[idx]["symptome"],
            "score": round(float(ähnlichkeit[idx]), 3)
        })
    return ergebnisse

# 🔹 Terminal-Eingabe (für Testzwecke)
if __name__ == "__main__":
    eingabe = input("Welche Beschwerden hast du? ").strip()

    treffer = finde_passende_pflanzen(eingabe)

    if not treffer:
        print("❌ Keine passenden Heilpflanzen gefunden.")
    else:
        print("\n🌿 Passende Heilpflanzen:")
        for pflanze in treffer:
            print(f"- {pflanze['name']} ({pflanze['score']}) → {pflanze['symptome']}")
