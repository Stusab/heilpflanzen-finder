import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import GermanStemmer
import nltk

nltk.download('punkt')  # nötig für Tokenisierung
nltk.download('punkt_tab')
# 🔹 Funktion zur Stemming-Vorverarbeitung
stemmer = GermanStemmer()

def stemme_text(text):
    tokens = nltk.word_tokenize(text.lower())
    return " ".join([stemmer.stem(t) for t in tokens])

# 🔹 CSV mit Symptomen laden
df = pd.read_csv("heilpflanzen_symptome_ready.csv")

# 🔹 Wende Stemming auf alle Symptome an
df["symptome_gestemmt"] = df["symptome"].apply(stemme_text)

# 🔹 TF-IDF auf gestemmte Texte
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["symptome_gestemmt"])

# 🔹 Funktion: Benutzertext → passende Pflanzen
def finde_passende_pflanzen(symptom_text, top_n=5):
    user_stemmed = stemme_text(symptom_text)
    user_vec = vectorizer.transform([user_stemmed])
    ähnlichkeit = cosine_similarity(user_vec, X).flatten()

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

# 🔹 Terminal-Eingabe
if __name__ == "__main__":
    symptomeingabe = input("Welche Beschwerden hast du? ").strip()

    if not symptomeingabe:
        print("❗ Bitte gib mindestens ein Symptom ein.")
    else:
        treffer = finde_passende_pflanzen(symptomeingabe)

        if not treffer:
            print("❌ Keine passenden Heilpflanzen gefunden.")
        else:
            print("\n🌿 Passende Heilpflanzen:")
            for eintrag in treffer:
                print(f"- {eintrag['name']} ({eintrag['score']}) → {eintrag['symptome']}")
