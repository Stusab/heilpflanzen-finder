import streamlit as st
import os
from logger import setup_logger
from version import __version__ as APP_VERSION

# Versuche das Modell zu importieren
try:
    from symptom_model import finde_passende_pflanzen
except ImportError as e:
    st.error("❌ Fehler beim Laden des Modells. Bitte prüfe, ob die Datei `symptom_model.py` vorhanden und korrekt ist.")
    raise e

# Logging setup
logger = setup_logger()

# Streamlit UI-Konfiguration
st.set_page_config(page_title="Heilpflanzen-Finder", layout="centered")
st.sidebar.markdown(f"**Version:** {APP_VERSION}")

st.title("🌿 Heilpflanzen-Finder")
st.write("Gib deine Beschwerden ein, und wir zeigen passende Heilpflanzen.")

# Formular-Eingabe
with st.form(key="symptom_form"):
    user_input = st.text_input("🩺 Welche Symptome hast du?", key="input_text")
    submit_button = st.form_submit_button(label="🔍 Suche starten")

if submit_button:
    if not user_input.strip():
        st.warning("⚠️ Bitte gib Symptome ein, bevor du suchst.")
    else:
        logger.info(f"Benutzereingabe: {user_input}")
        with st.spinner("🔄 Suche läuft..."):
            try:
                treffer = finde_passende_pflanzen(user_input)
            except Exception as e:
                st.error("❌ Fehler bei der Suche. Prüfe Logs für Details.")
                logger.error(f"Fehler bei der Verarbeitung: {e}")
                raise e

        if not treffer:
            st.warning("❌ Keine passenden Heilpflanzen gefunden.")
            logger.warning("Keine passenden Heilpflanzen gefunden.")
        else:
            st.success(f"✅ {len(treffer)} passende Heilpflanzen gefunden:")
            logger.info(f"{len(treffer)} Ergebnisse gefunden.")

            for eintrag in treffer:
                st.markdown(f"### 🌿 {eintrag['name']}")
                st.markdown(f"**Score:** {round(eintrag['score'], 2)}")
                st.markdown(f"{eintrag['symptome']}")
                st.markdown("---")
