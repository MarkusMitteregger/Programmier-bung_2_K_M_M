import streamlit as st
from PIL import Image
import test_a as a
import test_m as m

# Eine Überschrift der ersten Ebene
st.write("# PATIENTEN-DATENBANK")

# Laden Sie die Personendaten
person_data = a.Person.load_person_data()

# Legen Sie eine neue Liste mit den Personennamen an
patients = a.Person.get_person_list(person_data=person_data)

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
    st.session_state.picture_path = a.Person.find_person_data_by_name(st.session_state.current_user)["picture_path"]
else:
    st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'
    st.session_state.current_user = ""

# Öffne das Bild und zeige es an
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.current_user if 'current_user' in st.session_state else "")

# Prüfen, ob ein Patient ausgewählt wurde und EKG-Tests laden
if selected_patient != "Wählen Sie einen Patienten aus":
    patient_data = a.Person.find_person_data_by_name(selected_patient)
    ekg_tests = patient_data.get("ekg_tests", [])

    if ekg_tests:
        ekg_options = ["Wählen Sie einen Test aus"] + [f"Test-ID {ekg['id']}; Datum: {ekg['date']}" for ekg in ekg_tests]
    else:
        ekg_options = ["Noch keine EKG-Daten vorhanden"]

    selected_ekg = st.selectbox("Wählen Sie einen EKG-Test aus", options=ekg_options)

    if selected_ekg != "Wählen Sie einen Test aus" and selected_ekg != "Noch keine EKG-Daten vorhanden":
        # Extrahiere die EKG-ID sicher
        ekg_id = int(selected_ekg.split(" ")[1].replace(";", ""))
        ekg_data = m.EKGdata.load_by_id(ekg_id)

        if ekg_data:
            st.write(f"Durchschnittliche Herzfrequenz: {ekg_data.heartrate:.2f} bpm")
            ekg_data.make_plot()
        else:
            st.write("Keine EKG-Daten gefunden.")

    # Anlegen des Session State. Bild, wenn es kein Bild gibt'

    # Überprüfen, ob ein tatsächlicher Patient ausgewählt wurde
    if selected_ekg != "Wählen Sie einen Test aus":
        st.session_state.current_ekg = selected_ekg

        # Suchen des Ergebnislinks für den ausgewählten EKG-Test
        ekg_id = int(selected_ekg.split(" ")[1].replace(";", ""))
        result_link = None

        # Durchlaufen der EKG-Tests des ausgewählten Patienten, um den Ergebnislink zu finden
        for ekg_test in patient_data.get("ekg_tests", []):
            if ekg_test["id"] == ekg_id:
                result_link = ekg_test.get("result_link")
                break

        if result_link:
            st.write(f"Link zu den EKG-Daten: {result_link}")
        else:
            st.write("Kein Link gefunden.")
    else:
        st.write("Kein EKG-Test ausgewählt.")

    