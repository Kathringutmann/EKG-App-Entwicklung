import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name

person_data = get_person_data()
names = get_name(person_data)
    
#sessions State wird leer angelegt, solange 
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

st.title('EKG Analyse')
# Eine Überschrift der zweiten Ebene
st.write("## Versuchsperson auswählen")


current_user = st.selectbox(
    'Versuchsperson',
    options = names, key="sbVersuchspersonen")

st.write("currently selected user is: "+ current_user)

# Paket zum anzeigen der Bilder
from PIL import Image
# Laden eines Bilds
image = Image.open(find_person_data_by_name(current_user)["picture_path"])
# Anzeigen eines Bilds mit Caption
st.image(image, caption=st.session_state.current_user)


