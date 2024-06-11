import streamlit as st
import sqlite3

# Funzioni di utilità per la gestione del database
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS departments (id TEXT PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS units (id TEXT PRIMARY KEY, name TEXT, department_id TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS specialties (id TEXT PRIMARY KEY, name TEXT, unit_id TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS equipments (id TEXT PRIMARY KEY, name TEXT, specialty_id TEXT)''')
    conn.commit()
    conn.close()

def run_query(query, params=()):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute(query)
    data = c.fetchall()
    conn.close()
    return data

# Inizializza il database
init_db()

# Funzione principale
def main():
    st.title("Gestione Ospedale")
    menu = ["Home", "Reparti", "Unità Operative", "Specialità", "Apparecchiature"]
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

def manage_departments():
    st.subheader("Gestione Reparti")
    with st.form(key='department_form'):
        dept_id = st.text_input("ID Reparto")
        dept_name = st.text_input("Nome Reparto")
        submit_button = st.form_submit_button(label='Salva Reparto')

    if submit_button:
        run_query('INSERT OR REPLACE INTO departments (id, name) VALUES (?, ?)', (dept_id, dept_name))
        st.success(f"Reparto {dept_name} salvato con successo")

    departments = fetch_all('SELECT * FROM departments')
    if departments:
        st.subheader("Elenco Reparti")
        for dept_id, dept_name in departments:
            st.write(f"ID: {dept_id} - Nome: {dept_name}")
            if st.button(f"Modifica {dept_id}"):
                with st.form(key=f'department_edit_form_{dept_id}'):
                    new_dept_name = st.text_input("Nome Reparto", value=dept_name)
                    update_button = st.form_submit_button(label='Aggiorna Reparto')
                if update_button:
                    run_query('UPDATE departments SET name = ? WHERE id = ?', (new_dept_name, dept_id))
                    st.success(f"Reparto {dept_id} aggiornato con successo")
                    st.experimental_rerun()
            if st.button(f"Elimina {dept_id}"):
                run_query('DELETE FROM departments WHERE id = ?', (dept_id,))
                st.success(f"Reparto {dept_id} eliminato con successo")
                st.experimental_rerun()

def manage_units():
    st.subheader("Gestione Unità Operative")
    departments = fetch_all('SELECT * FROM departments')
    dept_options = {dept_id: dept_name for dept_id, dept_name in departments}

    with st.form(key='unit_form'):
        unit_id = st.text_input("ID Unità Operativa")
        unit_name = st.text_input("Nome Unità Operativa")
        dept_id = st.selectbox("Seleziona Reparto", list(dept_options.keys()), format_func=lambda x: dept_options[x])
        submit_button = st.form_submit_button(label='Salva Unità Operativa')

    if submit_button:
        run_query('INSERT OR REPLACE INTO units (id, name, department_id) VALUES (?, ?, ?)', (unit_id, unit_name, dept_id))
        st.success(f"Unità Operativa {unit_name} salvata con successo")

    units = fetch_all('SELECT * FROM units')
    if units:
        st.subheader("Elenco Unità Operative")
        for unit_id, unit_name, dept_id in units:
            st.write(f"ID: {unit_id} - Nome: {unit_name} - Reparto: {dept_options[dept_id]}")
            if st.button(f"Modifica {unit_id}"):
                with st.form(key=f'unit_edit_form_{unit_id}'):
                    new_unit_name = st.text_input("Nome Unità Operativa", value=unit_name)
                    new_dept_id = st.selectbox("Seleziona Reparto", list(dept_options.keys()), index=list(dept_options.keys()).index(dept_id), format_func=lambda x: dept_options[x])
                    update_button = st.form_submit_button(label='Aggiorna Unità Operativa')
                if update_button:
                    run_query('UPDATE units SET name = ?, department_id = ? WHERE id = ?', (new_unit_name, new_dept_id, unit_id))
                    st.success(f"Unità Operativa {unit_id} aggiornata con successo")
                    st.experimental_rerun()
            if st.button(f"Elimina {unit_id}"):
                run_query('DELETE FROM units WHERE id = ?', (unit_id,))
                st.success(f"Unità Operativa {unit_id} eliminata con successo")
                st.experimental_rerun()

def manage_specialties():
    st.subheader("Gestione Specialità")
    units = fetch_all('SELECT * FROM units')
    unit_options = {unit_id: unit_name for unit_id, unit_name, dept_id in units}

    with st.form(key='specialty_form'):
        spec_id = st.text_input("ID Specialità")
        spec_name = st.text_input("Nome Specialità")
        unit_id = st.selectbox("Seleziona Unità Operativa", list(unit_options.keys()), format_func=lambda x: unit_options[x])
        submit_button = st.form_submit_button(label='Salva Specialità')

    if submit_button:
        run_query('INSERT OR REPLACE INTO specialties (id, name, unit_id) VALUES (?, ?, ?)', (spec_id, spec_name, unit_id))
        st.success(f"Specialità {spec_name} salvata con successo")

    specialties = fetch_all('SELECT * FROM specialties')
    if specialties:
        st.subheader("Elenco Specialità")
        for spec_id, spec_name, unit_id in specialties:
            st.write(f"ID: {spec_id} - Nome: {spec_name} - Unità Operativa: {unit_options[unit_id]}")
            if st.button(f"Modifica {spec_id}"):
                with st.form(key=f'specialty_edit_form_{spec_id}'):
                    new_spec_name = st.text_input("Nome Specialità", value=spec_name)
                    new_unit_id = st.selectbox("Seleziona Unità Operativa", list(unit_options.keys()), index=list(unit_options.keys()).index(unit_id), format_func=lambda x: unit_options[x])
                    update_button = st.form_submit_button(label='Aggiorna Specialità')
                if update_button:
                    run_query('UPDATE specialties SET name = ?, unit_id = ? WHERE id = ?', (new_spec_name, new_unit_id, spec_id))
                    st.success(f"Specialità {spec_id} aggiornata con successo")
                    st.experimental_rerun()
            if st.button(f"Elimina {spec_id}"):
                run_query('DELETE FROM specialties WHERE id = ?', (spec_id,))
                st.success(f"Specialità {spec_id} eliminata con successo")
                st.experimental_rerun()

def manage_equipments():
    st.subheader("Gestione Apparecchiature")
    specialties = fetch_all('SELECT * FROM specialties')
    spec_options = {spec_id: spec_name for spec_id, spec_name, unit_id in specialties}

    with st.form(key='equipment_form'):
        equip_id = st.text_input("ID Apparecchiatura")
        equip_name = st.text_input("Nome Apparecchiatura")
        spec_id = st.selectbox("Seleziona Specialità", list(spec_options.keys()), format_func=lambda x: spec_options[x])
        submit_button = st.form_submit_button(label='Salva Apparecchiatura')

    if submit_button:
        run_query('INSERT OR REPLACE INTO equipments (id, name, specialty_id) VALUES (?, ?, ?)', (equip_id, equip_name, spec_id))
        st.success(f"Apparecchiatura {equip_name} salvata con successo")

    equipments = fetch_all('SELECT * FROM equipments')
    if equipments:
        st.subheader("Elenco Apparecchiature")
        for equip_id, equip_name, spec_id in equipments:
            st.write(f"ID: {equip_id} - Nome: {equip_name} - Specialità: {spec_options[spec_id]}")
            if st.button(f"Modifica {equip_id}"):
                with st.form(key=f'equipment_edit_form_{equip_id}'):
                    new_equip_name = st.text_input("Nome Apparecchiatura", value=equip_name)
                    new_spec_id = st.selectbox("Seleziona Specialità", list(spec_options.keys()), index=list(spec_options.keys()).index(spec_id), format_func=lambda x: spec_options[x])
                    update_button = st.form_submit_button(label='Aggiorna Apparecchiatura')
                if update_button:
                    run_query('UPDATE equipments SET name = ?, specialty_id = ? WHERE id = ?', (new_equip_name, new_spec_id, equip_id))
                    st.success(f"Apparecchiatura {equip_id} aggiornata con successo")
                    st.experimental_rerun()
            if st.button(f"Elimina {equip_id}"):
                run_query('DELETE FROM equipments WHERE id = ?', (equip_id,))
                st.success(f"Apparecchiatura {equip_id} eliminata con successo")
                st.experimental_rerun()

if __name__ == '__main__':
    main()
