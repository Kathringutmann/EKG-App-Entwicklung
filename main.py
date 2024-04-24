import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name

person_data = get_person_data()
names = get_name(person_data)
    
#sessions State wird leer angelegt, solange 
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    
#Überschrift
st.title('EKG Analyse')

from PIL import Image

col1, col2 = st.columns(2)

with col1:
   st.write("## Versuchsperson auswählen") #Unterüberschrift
   current_user = st.selectbox(
    'Versuchsperson',
    options = names, key="sbVersuchspersonen")#Auswahlbox
   image = Image.open(find_person_data_by_name(current_user)["picture_path"])

   st.write("currently selected user is: "+ current_user)

with col2:
   st.header("Bild")
   st.image(image, caption=st.session_state.current_user)
