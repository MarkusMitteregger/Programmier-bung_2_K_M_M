import streamlit as st
import read_data
from PIL import Image

# Eine Überschrift der ersten Ebene
st.write("# EKG APP")

# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")

# Legen Sie eine neue Liste mit den Personennamen an indem Sie ihre 
# Funktionen aufrufen
person_dict = read_data.load_person_data()
person_names = read_data.get_person_list(person_dict)

# Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
st.session_state.current_user = st.selectbox(
    'Versuchsperson',
    options=person_names, key="sbVersuchsperson"
)

# Search for the image path only if the name is known
if st.session_state.current_user in person_names:
    person_data = read_data.find_person_data_by_name(st.session_state.current_user)
    if person_data:
        st.session_state.picture_path = person_data["picture_path"]
    else:
        st.session_state.picture_path = 'data/pictures/none.jpg'
else:
    st.session_state.picture_path = 'data/pictures/none.jpg'

# Open the image and display it
image_path = "../" + st.session_state.picture_path
image = Image.open(image_path)
st.image(image, caption=st.session_state.current_user)
