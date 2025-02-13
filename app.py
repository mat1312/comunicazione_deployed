import streamlit as st
import json
import re
from openai import OpenAI

def replace_citations(text, citations):
    def citation_link(match):
        num_str = match.group(1)
        try:
            idx = int(num_str) - 1
            if 0 <= idx < len(citations):
                fonte = citations[idx]
                url = fonte.get("url", "") if isinstance(fonte, dict) else fonte
                return f"[{num_str}]({url})"
            else:
                return match.group(0)
        except Exception:
            return match.group(0)
    return re.sub(r'\[(\d+)\]', citation_link, text)

# CSS per i bottoni
st.markdown(
    """
    <style>
    div.stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

YOUR_API_KEY = "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"
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

st.title("📢 Analisi della posizione politica di Giorgia Meloni")
st.markdown("Seleziona l'argomento che desideri analizzare:")

col1, col2, col3, col4 = st.columns(4)

def display_response(response_data):
    risposta = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna risposta disponibile.")
    fonti = response_data.get("citations", [])
    
    st.subheader("📜 Risultato dell'analisi:")
    processed_text = replace_citations(risposta, fonti)
    st.markdown(processed_text, unsafe_allow_html=True)
    
    if fonti:
        st.subheader("🔗 Fonti Consultabili:")
        for i, fonte in enumerate(fonti, start=1):
            if isinstance(fonte, dict):
                nome = fonte.get("name", f"Fonte {i}")
                url = fonte.get("url", "#")
            else:
                nome = fonte
                url = fonte
            st.markdown(f"{i}. [{nome}]({url})", unsafe_allow_html=True)
    else:
        st.write("Nessuna fonte disponibile.")

# Inizializza la cronologia della conversazione (solo user e assistant)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def aggiorna_storia(ruolo, contenuto):
    """Aggiunge un messaggio alla cronologia della conversazione."""
    st.session_state.chat_history.append({"role": ruolo, "content": contenuto})

def esegui_richiesta(prompt):
    # Crea il messaggio di sistema e il messaggio corrente dell'utente
    messages = [
        {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        {"role": "user", "content": prompt},
    ]
    with st.spinner("Caricamento in corso..."):
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
        )
        response_data = json.loads(response.model_dump_json())
        display_response(response_data)
        
        # Estrai la risposta dell'assistente
        assistant_msg = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Aggiorna la cronologia con il turno completo (user e assistant)
        aggiorna_storia("user", prompt)
        aggiorna_storia("assistant", assistant_msg)
        
    return response_data

# Pulsanti per richieste predefinite
if col1.button("Autonomia Differenziata"):
    prompt = ("Com'è cambiata l'opinione di Giorgia Meloni sull'Autonomia Differenziata? "
              "Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero e spiega le eventuali ragioni politiche.")
    esegui_richiesta(prompt)

if col2.button("Reddito di Cittadinanza"):
    prompt = ("Com'è evoluta la posizione di Giorgia Meloni sul Reddito di Cittadinanza? "
              "Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero e spiega le eventuali ragioni politiche.")
    esegui_richiesta(prompt)

if col3.button("Bonus 110%"):
    prompt = ("Qual è la posizione di Giorgia Meloni sul Bonus 110%? "
              "Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero e spiega le eventuali ragioni politiche.")
    esegui_richiesta(prompt)

if col4.button("Presidenzialismo"):
    prompt = ("Com'è evoluta la posizione di Giorgia Meloni sul Presidenzialismo? "
              "Fornisci una timeline dettagliata e ben strutturata che illustri l'evoluzione del suo pensiero e spiega le eventuali ragioni politiche.")
    esegui_richiesta(prompt)

st.markdown("---")
st.subheader("Inserisci un prompt personalizzato")
custom_prompt = st.text_area("Scrivi qui il tuo prompt:")

if st.button("Invia il prompt"):
    if custom_prompt.strip() != "":
        # Costruiamo i messaggi partendo dal sistema e includendo la cronologia completa
        messages = [
            {"role": "system", "content": "Sei un'assistente AI italiana che risponde in modo dettagliato e cortese. Rispondi sempre con un formato leggibile e ben strutturato."},
        ]
        messages.extend(st.session_state.chat_history)
        messages.append({
            "role": "user",
            "content": f"""L'utente desidera un'analisi dettagliata cronologica della posizione di un partito o politico su un tema specifico.
Genera una timeline con una sintesi delle dichiarazioni più rilevanti.

Domanda dell'utente: {custom_prompt}

Risposta attesa: un elenco con header grandi e paragrafi dettagliati ordinato nel tempo con le principali dichiarazioni, cambi di posizione e sviluppi del dibattito pubblico. Rispondi sempre con un formato leggibile e ben strutturato."""
        })
        with st.spinner("Caricamento in corso..."):
            response = client.chat.completions.create(
                model="sonar-pro",
                messages=messages,
            )
            response_data = json.loads(response.model_dump_json())
            display_response(response_data)
            
            # Estrai la risposta dell'assistente e aggiorna la cronologia
            assistant_msg = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            aggiorna_storia("user", custom_prompt)
            aggiorna_storia("assistant", assistant_msg)
    else:
        st.error("Per favore, inserisci un prompt valido!")
