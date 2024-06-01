import streamlit as st
import read_data # Ergänzen Sie Ihr eigenes Modul
from PIL import Image
import test_a as a
import test_m as m 

# Eine Überschrift der ersten Ebene
st.write("# PATIENTEN-DATENBANK")

# Legen Sie eine neue Liste mit den Personennamen an indem Sie ihre 
patients = a.Person.get_person_list(person_data=a.Person.load_person_data())

# Fügen Sie einen Platzhalter für die Dropdown-Liste hinzu
patients.insert(0, "Wählen Sie einen Patienten aus")

# Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
selected_patient = st.selectbox("Wählen Sie einen Patienten aus", options=patients, key="sbVersuchsperson")

# Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'

# Überprüfen, ob ein tatsächlicher Patient ausgewählt wurde
if selected_patient != "Wählen Sie einen Patienten aus":
    st.session_state.current_user = selected_patient
    # Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
    st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]
else:
    st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg' 
    st.session_state.current_user = ""

# Öffne das Bild und Zeige es an
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.current_user if 'current_user' in st.session_state else "")


