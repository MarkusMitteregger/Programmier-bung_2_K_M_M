import streamlit as st
import read_data # Ergänzen Sie Ihr eigenes Modul
from PIL import Image

# Eine Überschrift der ersten Ebene
st.write("# PATIENTEN-DATENBANK")


# Legen Sie eine neue Liste mit den Personennamen an indem Sie ihre 
# Funktionen aufrufen
person_dict = read_data.load_person_data()
person_names = read_data.get_person_list(person_dict)
# bzw: wenn Sie nicht zwei separate Funktionen haben
# person_names = read_data.get_person_list()

# Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
st.session_state.current_user = st.selectbox("Wählen Sie einen Patienten aus",
    options = person_names, key="sbVersuchsperson")

    
# Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

# ...

# Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
if st.session_state.current_user in person_names:
    st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]

# ...

# Öffne das Bild und Zeige es an
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.current_user)

# Seitenleiste für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Gehe zu", ["Patienten-Datenbank", "EKG-Tests"])

if page == "EKG-Tests":
    # Legen Sie eine neue Liste mit den EKGs an indem Sie ihre 
# Funktionen aufrufen
    person_dict = read_data.load_person_data()
    print(person_dict)
        
        # Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
    st.session_state.current_user = st.selectbox(
        'EKG',
        options = [1,2,3])
    st.write("Hier kommt die EKG-Test Seite")