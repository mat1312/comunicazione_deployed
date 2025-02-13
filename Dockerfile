# Usa un'immagine Python leggera
FROM python:3.9-slim

# Imposta la cartella di lavoro
WORKDIR /app

# Copia i file necessari
COPY requirements.txt .
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta di Streamlit (Vercel imposta la porta come variabile d'ambiente)
EXPOSE $PORT

# Avvia Streamlit con i parametri necessari
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false
