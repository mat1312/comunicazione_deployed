import streamlit as st
import json
from openai import OpenAI

# Aggiungi custom CSS per rendere i bottoni a larghezza fissa e simmetrici
st.markdown(
    """
    <style>
    /* Imposta ogni bottone al 100% della larghezza della sua colonna */
    div.stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configura l'API Perplexity
YOUR_API_KEY = "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"
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

st.title("📢 Analisi della posizione politica di Giorgia Meloni")
st.markdown("Seleziona l'argomento che desideri analizzare:")

# Creazione di 4 colonne per i pulsanti (uguali in larghezza)
col1, col2, col3, col4 = st.columns(4)

# Pulsante per l'autonomia differenziata
if col1.button("Autonomia Differenziata"):
    messages = [
        {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        {"role": "user", "content": "Com'è cambiata l'opinione di Giorgia Meloni sull'Autonomia Differenziata? Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero su questo argomento e spiega le eventuali ragioni politiche."},
    ]
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    response_data = json.loads(response.model_dump_json())
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risposta dell'AI:")
    st.write(risposta)
    
    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for fonte in fonti:
            st.markdown(f"- [{fonte}]({fonte})")
    else:
        st.write("Nessuna fonte disponibile.")

# Pulsante per il Reddito di Cittadinanza
if col2.button("Reddito di Cittadinanza"):
    messages = [
        {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        {"role": "user", "content": "Com'è evoluta la posizione di Giorgia Meloni sul Reddito di Cittadinanza? Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero su questo argomento e spiega le eventuali ragioni politiche."},
    ]
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    response_data = json.loads(response.model_dump_json())
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risposta dell'AI:")
    st.write(risposta)
    
    
    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for fonte in fonti:
            st.markdown(f"- [{fonte}]({fonte})")
    else:
        st.write("Nessuna fonte disponibile.")

# Pulsante per il Bonus 110%
if col3.button("Bonus 110%"):
    messages = [
        {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        {"role": "user", "content": "Qual è la posizione di Giorgia Meloni sul Bonus 110%? Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero su questo argomento e spiega le eventuali ragioni politiche."},
    ]
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    response_data = json.loads(response.model_dump_json())
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risposta dell'AI:")
    st.write(risposta)
    
    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for fonte in fonti:
            st.markdown(f"- [{fonte}]({fonte})")
    else:
        st.write("Nessuna fonte disponibile.")

# Pulsante per il Presidenzialismo
if col4.button("Presidenzialismo"):
    messages = [
        {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        {"role": "user", "content": "Com'è evoluta la posizione di Giorgia Meloni sul Presidenzialismo? Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero su questo argomento e spiega le eventuali ragioni politiche."},
    ]
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    response_data = json.loads(response.model_dump_json())
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risposta dell'AI:")
    st.write(risposta)

    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for fonte in fonti:
            st.markdown(f"- [{fonte}]({fonte})")
    else:
        st.write("Nessuna fonte disponibile.")
