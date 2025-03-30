import streamlit as st
from symptom_model import finde_passende_pflanzen  # dein Suchmodell

st.set_page_config(page_title="Heilpflanzen-Finder", layout="centered")

st.title("🌿 Heilpflanzen-Finder")
st.write("Gib deine Beschwerden ein, und wir zeigen passende Heilpflanzen.")

# Formular für interaktive Suchfunktion
with st.form(key="symptom_form"):
    user_input = st.text_input("🩺 Welche Symptome hast du?", key="input_text")
    submit_button = st.form_submit_button(label="🔍 Suche starten")

# Nur wenn der Button gedrückt wurde, wird gesucht
if submit_button and user_input:
    treffer = finde_passende_pflanzen(user_input)

    if not treffer:
        st.warning("❌ Keine passenden Heilpflanzen gefunden.")
    else:
        st.success(f"✅ {len(treffer)} passende Heilpflanzen gefunden:")
        for eintrag in treffer:
            st.markdown(f"### 🌿 {eintrag['name']}")
            st.markdown(f"**Score:** {round(eintrag['score'], 2)}")
            st.markdown(f"{eintrag['symptome']}")
            st.markdown("---")
