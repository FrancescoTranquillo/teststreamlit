import streamlit as st
import sqlite3
import pandas as pd

# Funzione per creare le tabelle
def create_tables():
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('''
                      CREATE TABLE IF NOT EXISTS departments
                      (id TEXT PRIMARY KEY, name TEXT)
                      ''')
            c.execute('''
                      CREATE TABLE IF NOT EXISTS units
                      (id TEXT PRIMARY KEY, name TEXT, department_id TEXT,
                      FOREIGN KEY(department_id) REFERENCES departments(id))
                      ''')
            c.execute('''
                      CREATE TABLE IF NOT EXISTS specialties
                      (id TEXT PRIMARY KEY, name TEXT, unit_id TEXT,
                      FOREIGN KEY(unit_id) REFERENCES units(id))
                      ''')
            c.execute('''
                      CREATE TABLE IF NOT EXISTS equipments
                      (id TEXT PRIMARY KEY, name TEXT, specialty_id TEXT, price REAL, quantity INTEGER,
                      FOREIGN KEY(specialty_id) REFERENCES specialties(id))
                      ''')
            conn.commit()
    except Exception as e:
        st.error(f"Errore nella creazione delle tabelle: {e}")

# Esegui la funzione per creare le tabelle all'avvio dell'app
create_tables()

# Funzioni per gestire le operazioni CRUD
def add_department(id, name):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO departments (id, name) VALUES (?, ?)', (id, name))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiunta del reparto: {e}")

def add_unit(id, name, department_id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO units (id, name, department_id) VALUES (?, ?, ?)', (id, name, department_id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiunta dell'unità operativa: {e}")

def add_specialty(id, name, unit_id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO specialties (id, name, unit_id) VALUES (?, ?, ?)', (id, name, unit_id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiunta della specialità: {e}")

def add_equipment(id, name, specialty_id, price, quantity):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO equipments (id, name, specialty_id, price, quantity) VALUES (?, ?, ?, ?, ?)', (id, name, specialty_id, price, quantity))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiunta dell'apparecchiatura: {e}")

def update_department(id, name):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE departments SET name = ? WHERE id = ?', (name, id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiornamento del reparto: {e}")

def update_unit(id, name, department_id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE units SET name = ?, department_id = ? WHERE id = ?', (name, department_id, id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiornamento dell'unità operativa: {e}")

def update_specialty(id, name, unit_id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE specialties SET name = ?, unit_id = ? WHERE id = ?', (name, unit_id, id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiornamento della specialità: {e}")

def update_equipment(id, name, specialty_id, price, quantity):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE equipments SET name = ?, specialty_id = ?, price = ?, quantity = ? WHERE id = ?', (name, specialty_id, price, quantity, id))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'aggiornamento dell'apparecchiatura: {e}")

def delete_department(id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM departments WHERE id = ?', (id,))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'eliminazione del reparto: {e}")

def delete_unit(id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM units WHERE id = ?', (id,))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'eliminazione dell'unità operativa: {e}")

def delete_specialty(id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM specialties WHERE id = ?', (id,))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'eliminazione della specialità: {e}")

def delete_equipment(id):
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('DELETE FROM equipments WHERE id = ?', (id,))
            conn.commit()
    except Exception as e:
        st.error(f"Errore nell'eliminazione dell'apparecchiatura: {e}")

def get_departments():
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM departments')
            return c.fetchall()
    except Exception as e:
        st.error(f"Errore nel recupero dei reparti: {e}")
        return []

def get_units():
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM units')
            return c.fetchall()
    except Exception as e:
        st.error(f"Errore nel recupero delle unità operative: {e}")
        return []

def get_specialties():
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM specialties')
            return c.fetchall()
    except Exception as e:
        st.error(f"Errore nel recupero delle specialità: {e}")
        return []

def get_equipments():
    try:
        with sqlite3.connect('hospital.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM equipments')
            return c.fetchall()
    except Exception as e:
        st.error(f"Errore nel recupero delle apparecchiature: {e}")
        return []

def main():
    st.title("Gestione Ospedale")
    menu = ["Home", "Reparti", "Unità Operative", "Specialità", "Apparecchiature", "Visualizza Configurazione"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Benvenuto nel sistema di gestione dell'ospedale.")
    
    elif choice == "Reparti":
        manage_departments()
    
    elif choice == "Unità Operative":
        manage_units()
    
    elif choice == "Specialità":
        manage_specialties()
    
    elif choice == "Apparecchiature":
        manage_equipments()

    elif choice == "Visualizza Configurazione":
        view_configuration()

def manage_departments():
    st.subheader("Gestione Reparti")
    with st.form(key='department_form'):
        dept_id = st.text_input("ID Reparto")
        dept_name = st.text_input("Nome Reparto")
        submit_button = st.form_submit_button(label='Salva Reparto')

    if submit_button:
        if dept_id in [d[0] for d in get_departments()]:
            update_department(dept_id, dept_name)
            st.success(f"Reparto {dept_name} aggiornato con successo")
        else:
            add_department(dept_id, dept_name)
            st.success(f"Reparto {dept_name} aggiunto con successo")

    if get_departments():
        st.subheader("Elenco Reparti")
        for dept_id, dept_name in get_departments():
            st.write(f"ID: {dept_id} - Nome: {dept_name}")
            if st.button(f"Elimina {dept_name}", key=f"del_dept_{dept_id}"):
                delete_department(dept_id)
                st.success(f"Reparto {dept_name} eliminato con successo")

def manage_units():
    st.subheader("Gestione Unità Operative")
    with st.form(key='unit_form'):
        unit_id = st.text_input("ID Unità Operativa")
        unit_name = st.text_input("Nome Unità Operativa")
        dept_id = st.selectbox("Seleziona Reparto", [d[0] for d in get_departments()])
        submit_button = st.form_submit_button(label='Salva Unità Operativa')

    if submit_button:
        if unit_id in [u[0] for u in get_units()]:
            update_unit(unit_id, unit_name, dept_id)
            st.success(f"Unità Operativa {unit_name} aggiornata con successo")
        else:
            add_unit(unit_id, unit_name, dept_id)
            st.success(f"Unità Operativa {unit_name} aggiunta con successo")

    if get_units():
        st.subheader("Elenco Unità Operative")
        for unit_id, unit_name, dept_id in get_units():
            st.write(f"ID: {unit_id} - Nome: {unit_name} - Reparto: {dept_id}")
            if st.button(f"Elimina {unit_name}", key=f"del_unit_{unit_id}"):
                delete_unit(unit_id)
                st.success(f"Unità Operativa {unit_name} eliminata con successo")

def manage_specialties():
    st.subheader("Gestione Specialità")
    with st.form(key='specialty_form'):
        spec_id = st.text_input("ID Specialità")
        spec_name = st.text_input("Nome Specialità")
        unit_id = st.selectbox("Seleziona Unità Operativa", [u[0] for u in get_units()])
        submit_button = st.form_submit_button(label='Salva Specialità')

    if submit_button:
        if spec_id in [s[0] for s in get_specialties()]:
            update_specialty(spec_id, spec_name, unit_id)
            st.success(f"Specialità {spec_name} aggiornata con successo")
        else:
            add_specialty(spec_id, spec_name, unit_id)
            st.success(f"Specialità {spec_name} aggiunta con successo")

    if get_specialties():
        st.subheader("Elenco Specialità")
        for spec_id, spec_name, unit_id in get_specialties():
            st.write(f"ID: {spec_id} - Nome: {spec_name} - Unità Operativa: {unit_id}")
            if st.button(f"Elimina {spec_name}", key=f"del_spec_{spec_id}"):
                delete_specialty(spec_id)
                st.success(f"Specialità {spec_name} eliminata con successo")

def manage_equipments():
    st.subheader("Gestione Apparecchiature")
    with st.form(key='equipment_form'):
        equip_id = st.text_input("ID Apparecchiatura")
        equip_name = st.text_input("Nome Apparecchiatura")
        spec_id = st.selectbox("Seleziona Specialità", [s[0] for s in get_specialties()])
        price = st.number_input("Prezzo", min_value=0.0, format="%.2f")
        quantity = st.number_input("Quantità", min_value=0)
        submit_button = st.form_submit_button(label='Salva Apparecchiatura')

    if submit_button:
        if equip_id in [e[0] for e in get_equipments()]:
            update_equipment(equip_id, equip_name, spec_id, price, quantity)
            st.success(f"Apparecchiatura {equip_name} aggiornata con successo")
        else:
            add_equipment(equip_id, equip_name, spec_id, price, quantity)
            st.success(f"Apparecchiatura {equip_name} aggiunta con successo")

    if get_equipments():
        st.subheader("Elenco Apparecchiature")
        for equip_id, equip_name, spec_id, price, quantity in get_equipments():
            st.write(f"ID: {equip_id} - Nome: {equip_name} - Specialità: {spec_id} - Prezzo: {price} - Quantità: {quantity}")
            if st.button(f"Elimina {equip_name}", key=f"del_equip_{equip_id}"):
                delete_equipment(equip_id)
                st.success(f"Apparecchiatura {equip_name} eliminata con successo")

def view_configuration():
    st.subheader("Configurazione Ospedale")
    
    departments = pd.DataFrame(get_departments(), columns=["ID Reparto", "Nome Reparto"])
    units = pd.DataFrame(get_units(), columns=["ID Unità Operativa", "Nome Unità Operativa", "ID Reparto"])
    specialties = pd.DataFrame(get_specialties(), columns=["ID Specialità", "Nome Specialità", "ID Unità Operativa"])
    equipments = pd.DataFrame(get_equipments(), columns=["ID Apparecchiatura", "Nome Apparecchiatura", "ID Specialità", "Prezzo", "Quantità"])

    st.write("## Reparti")
    st.table(departments)
    
    st.write("## Unità Operative")
    st.table(units)
    
    st.write("## Specialità")
    st.table(specialties)
    
    st.write("## Apparecchiature")
    st.table(equipments)

if __name__ == '__main__':
    main()
