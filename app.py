import streamlit as st

# Strutture dati in-memory
hospitals = {}
departments = {}
units = {}
specialties = {}
equipments = {}

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
        departments[dept_id] = dept_name
        st.success(f"Reparto {dept_name} aggiunto con successo")

    if departments:
        st.subheader("Elenco Reparti")
        for dept_id, dept_name in departments.items():
            st.write(f"ID: {dept_id} - Nome: {dept_name}")

def manage_units():
    st.subheader("Gestione Unità Operative")
    with st.form(key='unit_form'):
        unit_id = st.text_input("ID Unità Operativa")
        unit_name = st.text_input("Nome Unità Operativa")
        dept_id = st.selectbox("Seleziona Reparto", list(departments.keys()))
        submit_button = st.form_submit_button(label='Salva Unità Operativa')

    if submit_button:
        units[unit_id] = {"name": unit_name, "department": dept_id}
        st.success(f"Unità Operativa {unit_name} aggiunta con successo")

    if units:
        st.subheader("Elenco Unità Operative")
        for unit_id, unit_info in units.items():
            st.write(f"ID: {unit_id} - Nome: {unit_info['name']} - Reparto: {departments[unit_info['department']]}")

def manage_specialties():
    st.subheader("Gestione Specialità")
    with st.form(key='specialty_form'):
        spec_id = st.text_input("ID Specialità")
        spec_name = st.text_input("Nome Specialità")
        unit_id = st.selectbox("Seleziona Unità Operativa", list(units.keys()))
        submit_button = st.form_submit_button(label='Salva Specialità')

    if submit_button:
        specialties[spec_id] = {"name": spec_name, "unit": unit_id}
        st.success(f"Specialità {spec_name} aggiunta con successo")

    if specialties:
        st.subheader("Elenco Specialità")
        for spec_id, spec_info in specialties.items():
            st.write(f"ID: {spec_id} - Nome: {spec_info['name']} - Unità Operativa: {units[spec_info['unit']]['name']}")

def manage_equipments():
    st.subheader("Gestione Apparecchiature")
    with st.form(key='equipment_form'):
        equip_id = st.text_input("ID Apparecchiatura")
        equip_name = st.text_input("Nome Apparecchiatura")
        spec_id = st.selectbox("Seleziona Specialità", list(specialties.keys()))
        submit_button = st.form_submit_button(label='Salva Apparecchiatura')

    if submit_button:
        equipments[equip_id] = {"name": equip_name, "specialty": spec_id}
        st.success(f"Apparecchiatura {equip_name} aggiunta con successo")

    if equipments:
        st.subheader("Elenco Apparecchiature")
        for equip_id, equip_info in equipments.items():
            st.write(f"ID: {equip_id} - Nome: {equip_info['name']} - Specialità: {specialties[equip_info['specialty']]['name']}")

if __name__ == '__main__':
    main()
