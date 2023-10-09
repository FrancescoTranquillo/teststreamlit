# Importa le librerie necessarie
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Titolo dell'app
st.title("App di Streamlit per Visualizzare un Grafico")

# Descrizione dell'app
st.write("Questo è un esempio di un'app di Streamlit che visualizza un grafico.")

# Creazione di dati di esempio
data = pd.DataFrame({
    'x': np.arange(100),
    'y': np.random.randn(100)
})

# Opzione per visualizzare i dati
if st.checkbox("Mostra i dati"):
    st.write(data)

# Opzione per visualizzare il grafico
if st.checkbox("Mostra il grafico"):
    # Creazione del grafico
    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    st.pyplot(fig)

# Aggiungere ulteriori funzionalità o grafici all'app secondo necessità
