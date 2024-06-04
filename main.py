import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person
import ekgdata

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
    options = names, key="sbVersuchspersonen") #Auswahlbox
   
   current_person = person.Person(find_person_data_by_name(current_user))
   test_ids = person.Person.get_test_ids(current_person)
     
   
   image = Image.open(current_person.picture_path)
   

   st.write("currently selected user is: "+ current_user)
   st.write("age of current user: " + str(current_person.get_age()))
   st.write ("max heartrate calculated by age is: "+ str(current_person.calc_max_hr()))

with col2:
   st.header("Bild")
   st.image(image, caption=current_user)
   
   selected_test_id = st.selectbox('Wählen Sie eine Test-ID:', test_ids)

   st.write(f'Sie haben die Test-ID {selected_test_id} ausgewählt.')


   test_dict = ekgdata.EKGdata.load_by_id(person_data,selected_test_id)
   ekg = ekgdata.EKGdata(test_dict)
   
   ekg.find_peaks()
   ekg.make_plot()
   y_min = st.slider("EKG Frame Range", 0, 200000, 1000)#Slider löschen???
   y_min = st.slider("Untere Grenze", 0, 100, 0)
   y_max = st.slider("Obere Grenze", 0, 100, 100)#Slider anpassen... zusammen fügen, damit die zwei verbunden sind und parallel verschiebbar sind
   st.write(f"Der ausgewählte Wert ist: {y_min}")
   ekg.update_axis(y_min,5000)
   
   st.plotly_chart(ekg.fig)