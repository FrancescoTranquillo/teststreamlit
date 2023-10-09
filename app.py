import streamlit as st
import pandas as pd
import numpy as np

# Carica i dati dal tuo dataset
data = pd.read_csv("tuo_dataset.csv")  # Assicurati di inserire il percorso corretto al tuo dataset

# Titolo dell'app
st.title("Configuratore Apparecchiature Mediche")

# Seleziona i reparti e il numero desiderato
reparti_selezionati = st.multiselect("Seleziona i reparti desiderati:", data["Reparto"].unique())
numero_reparti = st.slider("Numero di reparti:", min_value=1, max_value=10, value=1)

# Filtra i dati in base ai reparti selezionati
data_filtrati = data[data["Reparto"].isin(reparti_selezionati)].copy()

# Crea una tabella con l'elenco delle apparecchiature
st.write(f"Elenco delle apparecchiature per {numero_reparti} reparti selezionati:")
st.dataframe(data_filtrati[["Specialità/Area", "Descrizione", "Quantità", "Importo unitario", "Totale"]])

# Calcola il totale economico
totale_economico = data_filtrati["Totale"].sum()

# Calcola il totale tecnico
elenco_apparecchiature_tecniche = data_filtrati["Descrizione"].tolist()

# Visualizza il totale economico e tecnico
st.write(f"Totale Economico: {totale_economico} €")
st.write("Elenco delle apparecchiature tecniche:")
for apparecchiatura in elenco_apparecchiature_tecniche:
    st.write(apparecchiatura)

# Salvataggio di un report in un file CSV
if st.button("Genera Report CSV"):
    report = pd.DataFrame({"Reparto": reparti_selezionati, "Totale Economico": [totale_economico] * len(reparti_selezionati)})
    report.to_csv("report.csv", index=False)
    st.success("Report CSV generato con successo.")

# Salvataggio di un report in un file di testo
if st.button("Genera Report Testo"):
    with open("report.txt", "w") as file:
        file.write(f"Totale Economico per {numero_reparti} reparti selezionati: {totale_economico} €\n")
        file.write("Elenco delle apparecchiature tecniche:\n")
        for apparecchiatura in elenco_apparecchiature_tecniche:
            file.write(f"- {apparecchiatura}\n")
    st.success("Report di testo generato con successo.")
