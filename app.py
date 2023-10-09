import streamlit as st
import pandas as pd
import numpy as np
from collections import defaultdict

# Carica i dati dal tuo dataset
uploaded_file = st.file_uploader("Choose a file")
data = pd.read_csv(uploaded_file, sep=';')
data["Totale"] = data["Totale"].str.replace("€", "").str.replace(".", "").astype(float)

# Crea una colonna vuota per le quantità personalizzate
data["Quantità personalizzate"] = 0

# Titolo dell'app
st.title("Configuratore GSD Tecnologie Medicali")

# Seleziona i reparti e il numero desiderato
reparti_selezionati = st.multiselect("Seleziona i reparti desiderati:", data["Reparto"].unique())
numero_reparti = st.slider("Numero di reparti:", min_value=1, max_value=10, value=1)

# Crea un dizionario per le specialità selezionate per ciascun reparto
specialita_per_reparto = {}
for reparto in reparti_selezionati:
    specialita_selezionate = st.multiselect(f"Seleziona le specialità per il reparto '{reparto}':", data[data["Reparto"] == reparto]["Specialità/Area"].unique())
    specialita_per_reparto[reparto] = specialita_selezionate

# Filtra i dati in base ai reparti e alle specialità selezionate
data_filtrati = data[(data["Reparto"].isin(reparti_selezionati)) & (data["Specialità/Area"].isin(specialita_per_reparto[reparto] for reparto in specialita_per_reparto))].copy()

# Crea una tabella con l'elenco delle apparecchiature e campi di input per le quantità personalizzate
st.write(f"Elenco delle apparecchiature per {numero_reparti} reparti selezionati:")
for index, row in data_filtrati.iterrows():
    quantita_personalizzata = st.number_input(f"Quantità per {row['Descrizione']}:", value=0)
    data_filtrati.at[index, "Quantità personalizzate"] = quantita_personalizzata

# Calcola il totale economico basato sulle quantità personalizzate
totale_economico = (data_filtrati["Quantità personalizzate"] * data_filtrati["Totale"]).sum()

# Raggruppa le apparecchiature per categoria e calcola le somme
categorie_apparecchiature = defaultdict(int)
for index, row in data_filtrati.iterrows():
    categoria = row["Categoria"]
    quantita = row["Quantità personalizzate"]
    totale = row["Totale"]
    categorie_apparecchiature[categoria] += quantita

# Raggruppa l'elenco tecnico per categoria
elenco_apparecchiature_tecniche = defaultdict(list)
for index, row in data_filtrati.iterrows():
    categoria = row["Categoria"]
    descrizione = row["Descrizione"]
    elenco_apparecchiature_tecniche[categoria].append(descrizione)

# Visualizza il riassunto delle apparecchiature per categoria
st.write("Riassunto delle apparecchiature per categoria:")
for categoria, quantita in categorie_apparecchiature.items():
    st.write(f"- {categoria}: Quantità totale: {quantita}, Totale Economico: € {quantita * totale_economico:.0f}")

# Visualizza il totale economico
st.write(f"Totale Economico: € {totale_economico:.0f}")

# Visualizza l'elenco tecnico raggruppato per categoria
st.write("Elenco delle apparecchiature tecniche:")
for categoria, elenco in elenco_apparecchiature_tecniche.items():
    st.write(f"- {categoria}:")
    for apparecchiatura in elenco:
        st.write(f"  - {apparecchiatura}")

# Salvataggio di un report in un file CSV
if st.button("Genera Report CSV"):
    report = pd.DataFrame({"Reparto": reparti_selezionati, "Totale Economico": [totale_economico] * len(reparti_selezionati)})
    report.to_csv("report.csv", index=False)
    st.success("Report CSV generato con successo.")

# Salvataggio di un report in un file di testo
if st.button("Genera Report Testo"):
    with open("report.txt", "w") as file:
        file.write(f"Totale Economico per {numero_reparti} reparti selezionati: € {totale_economico:.0f}\n")
        file.write("Riassunto delle apparecchiature per categoria:\n")
        for categoria, quantita in categorie_apparecchiature.items():
            file.write(f"- {categoria}: Quantità totale: {quantita}, Totale Economico: € {quantita * totale_economico:.0f}\n")
        file.write("Elenco delle apparecchiature tecniche:\n")
        for categoria, elenco in elenco_apparecchiature_tecniche.items():
            file.write(f"- {categoria}:\n")
            for apparecchiatura in elenco:
                file.write(f"  - {apparecchiatura}\n")
    st.success("Report di testo generato con successo.")
