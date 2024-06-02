import streamlit as st
from PIL import Image
import test_a as a
import test_m as m
import pandas as pd
import plotly.graph_objects as go

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

    # Anlegen des Session State. Bild, wenn es kein Bild gibt
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

    # Prüfen, ob ein Patient ausgewählt wurde und Leistungstest laden
if selected_patient != "Wählen Sie einen Patienten aus":
    patient_data = a.Person.find_person_data_by_name(selected_patient)
    intervall_tests = patient_data.get("intervall_tests", {})

    if intervall_tests:
        intervall_test_option = ["Wählen Sie einen Test aus"] + [f"Test-ID {intervall_tests['id']}; Datum: {intervall_tests['date']}"]
    else:
        intervall_test_option = ["Noch kein Leistungstest vorhanden"]

    selected_intervall_test = st.selectbox("Wählen Sie einen Leistungstest aus", options=intervall_test_option)

    if selected_intervall_test != "Wählen Sie einen Test aus" and selected_intervall_test != "Noch kein Leistungstest vorhanden":
        intervall_test_id = int(selected_intervall_test.split(" ")[1].replace(";", ""))
        
        def get_heart_rate_zone(heart_rate, max_hr):
            if heart_rate < 0.6 * max_hr:
                return 'Zone1'
            elif heart_rate < 0.7 * max_hr:
                return 'Zone2'
            elif heart_rate < 0.8 * max_hr:
                return 'Zone3'
            elif heart_rate < 0.9 * max_hr:
                return 'Zone4'
            else:
                return 'Zone5'

        # Funktion zur Analyse der Herzfrequenz
        def analyze_heart_rate(df, max_hr):
            df['HeartRateZone'] = df['HeartRate'].apply(lambda x: get_heart_rate_zone(x, max_hr))
            time_in_zones = df.groupby('HeartRateZone')['Duration'].sum()
            time_in_zones = time_in_zones.apply(lambda x: '{:02}:{:02}'.format(int(x) // 60, int(x) % 60))
            return time_in_zones

        # Funktion zur Analyse der Leistung
        def analyze_performance(df):
            avg_performance_in_zones = df.groupby('HeartRateZone')['PowerOriginal'].mean()
            avg_performance_in_zones = avg_performance_in_zones.round().astype(int)
            return avg_performance_in_zones


        st.title('Herzfrequenzanalyse')
        for intervall_test in [intervall_tests]:
            if intervall_test["id"] == intervall_test_id:
                dateipfad = intervall_test.get("result_link")


                df = pd.read_csv(dateipfad)
                max_hr = st.sidebar.number_input("Bitte geben Sie die maximale Herzfrequenz ein:", value=0, step=1)
                analyze_button = st.sidebar.button("Analyse durchführen")

                if analyze_button:
                    time_in_zones = analyze_heart_rate(df, max_hr)
                    avg_performance_in_zones = analyze_performance(df)
                    avg_performance_generel = df['PowerOriginal'].mean().round().astype(int)
                    max_performance_generel = df['PowerOriginal'].max().round().astype(int)

                    st.subheader('Zeit in HF-Zonen (in mm˸ss):')
                    st.write(time_in_zones)
                    st.subheader('Durchschnittliche Leistung in den Herzfrequenzzonen (in Watt):')
                    st.write(avg_performance_in_zones)
                    st.subheader('Durchschnittliche Leistung gesamt (in Watt):')
                    st.write(avg_performance_generel)
                    st.subheader('Maximale Leistung (in Watt):')
                    st.write(max_performance_generel)

                    time = df.index / 60

                    fig = go.Figure()

                    # Herzfrequenz und Leistung über die Zeit plotten
                    fig.add_trace(go.Scatter(x=time, y=df['HeartRate'], mode='lines', name='Heart Rate'))
                    fig.add_trace(go.Scatter(x=time, y=df['PowerOriginal'], mode='lines', name='Power'))

                    # Herzfrequenzzonen als Bereiche hinzufügen
                    fig.add_hrect(y0=0, y1=0.6*max_hr, fillcolor="lightblue", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.6*max_hr, y1=0.7*max_hr, fillcolor="lightgreen", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.7*max_hr, y1=0.8*max_hr, fillcolor="yellow", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.8*max_hr, y1=0.9*max_hr, fillcolor="orange", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.9*max_hr, y1=1.0*max_hr, fillcolor="red", opacity=0.2, line_width=0)

                    fig.update_layout(
                        title="Leistung und Herzfrequenz über die Zeit",
                        xaxis_title='Dauer [min]',
                        yaxis_title='Herzfrequenz [bpm], Leistung [W]'
                    )

                    st.plotly_chart(fig)

