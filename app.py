import streamlit as st
import json
import re
from openai import OpenAI

def replace_citations(text, citations):
    """
    Cerca nel testo tutte le occorrenze del pattern [numero] e, se esiste
    un URL corrispondente nella lista citations (assumendo che la prima fonte
    corrisponda a [1], la seconda a [2], ...), sostituisce il riferimento con
    un link markdown cliccabile.
    """
    def citation_link(match):
        num_str = match.group(1)
        try:
            idx = int(num_str) - 1
            if 0 <= idx < len(citations):
                # Se la fonte è un dizionario con 'name' e 'url', usa l'URL
                fonte = citations[idx]
                if isinstance(fonte, dict):
                    url = fonte.get("url", "")
                else:
                    url = fonte
                # Restituisce un link markdown, es. [10](http://...)
                return f"[{num_str}]({url})"
            else:
                return match.group(0)
        except Exception:
            return match.group(0)
    return re.sub(r'\[(\d+)\]', citation_link, text)

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

def display_response(response_data):
    # Estrae il testo della risposta
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    # Estrae l'elenco delle fonti (si assume che possa essere una lista di stringhe o di dizionari)
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risultato dell'analisi:")
    # Sostituisce i riferimenti nel testo con dei link cliccabili
    processed_text = replace_citations(risposta, fonti)
    st.markdown(processed_text, unsafe_allow_html=True)
    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for i, fonte in enumerate(fonti, start=1):
            # Se la fonte è un dizionario con chiavi "name" e "url", usale; altrimenti usa il valore intero
            if isinstance(fonte, dict):
                nome = fonte.get("name", f"Fonte {i}")
                url = fonte.get("url", "#")
            else:
                nome = fonte
                url = fonte
            st.markdown(f"{i}. [{nome}]({url})", unsafe_allow_html=True)
    else:
        st.write("Nessuna fonte disponibile.")

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
    display_response(response_data)

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
    display_response(response_data)

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
    display_response(response_data)

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
    display_response(response_data)
