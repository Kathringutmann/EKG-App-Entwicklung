import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person

#person_data = get_person_data()
#names = get_name(person_data)

person_data = person.Person.load_person_data()
names = person.Person.get_person_list(person_data)
    
current_person = None  
    
#Überschrift
st.title('EKG Analyse')

from PIL import Image

col1, col2 = st.columns(2)

with col1:
   st.write("## Versuchsperson auswählen") #Unterüberschrift
   current_user = st.selectbox(
    'Versuchsperson',
    options = names, key="sbVersuchspersonen")#Auswahlbox
   
   current_person = person.Person(find_person_data_by_name(current_user))

     
   
   image = Image.open(current_person.picture_path)
   

   st.write("currently selected user is: "+ current_user)
   st.write(current_person.get_age())
   st.write("currently selected user is: "+ current_person.calc_max_hr())

with col2:
   st.header("Bild")
   st.image(image, caption=current_user)
