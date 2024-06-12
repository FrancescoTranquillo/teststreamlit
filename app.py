import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import joblib
import os

# Funzione per addestrare il modello
def train_model(data, text_column, label_column):
    X = data[text_column]
    y = data[label_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy

# Funzione per categorizzare i testi
def categorize_texts(model, texts):
    return model.predict(texts)

# Caricare il file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type="csv")

if uploaded_file is not None:
    try:
        # Prova a leggere il file con la codifica UTF-8
        df = pd.read_csv(uploaded_file, encoding='utf-8', delimiter=',')
    except UnicodeDecodeError:
        try:
            # Prova a leggere il file con la codifica ISO-8859-1
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', delimiter=',')
        except Exception as e:
            st.error(f"Errore durante la lettura del file: {e}")
    except pd.errors.EmptyDataError:
        st.error("Il file caricato è vuoto.")
    except pd.errors.ParserError:
        st.error("Errore di parsing durante la lettura del file.")
    except Exception as e:
        st.error(f"Errore durante la lettura del file: {e}")
    else:
        if df.empty:
            st.error("Il file caricato è vuoto o non contiene colonne parsabili.")
        else:
            st.write("Ecco i dati caricati:")
            st.dataframe(df)

            # Selezionare la colonna del testo e la colonna delle categorie
            text_column = st.selectbox("Seleziona la colonna del testo", df.columns)
            label_column = st.selectbox("Seleziona la colonna delle categorie", df.columns)
            
            if st.button("Addestra il modello"):
                with st.spinner("Addestramento del modello in corso..."):
                    model, accuracy = train_model(df, text_column, label_column)
                    joblib.dump(model, 'text_classifier_model.pkl')
                    st.success(f"Modello addestrato con successo! Precisione: {accuracy:.2f}")
            
            # Caricare il modello addestrato
            if os.path.exists('text_classifier_model.pkl'):
                model = joblib.load('text_classifier_model.pkl')

                # Applicare il modello ai dati e creare il file CSV in uscita
                if st.button("Categorizza i testi"):
                    with st.spinner("Categorizzazione dei testi in corso..."):
                        df['Predicted_Category'] = categorize_texts(model, df[text_column])
                        output_file = "categorized_texts.csv"
                        df.to_csv(output_file, index=False)
                        st.success(f"Testi categorizzati con successo! Scarica il file {output_file} qui sotto:")
                        with open(output_file, "rb") as file:
                            st.download_button("Scarica il file CSV", data=file, file_name=output_file)
            else:
                st.warning("Il modello non è stato addestrato. Per favore addestra il modello prima di categorizzare i testi.")
