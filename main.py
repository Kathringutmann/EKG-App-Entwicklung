import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person
from ekgdata import EKGdata
from PIL import Image #Bibliothek für Bilder


person_data = person.Person.load_person_data() #Personendaten laden
names = person.Person.get_person_list(person_data) #Namen der Personen in Liste speichern
    
current_person = None  #Variable für aktuelle Person
    
#Überschrift
st.title('EKG Analyse')

col1, col2 = st.columns(2) #Spalten erstellen

with col1:
   st.write("## Versuchsperson auswählen") #Unterüberschrift
   current_user = st.selectbox(
    'Versuchsperson',
    options = names, key="sbVersuchspersonen") #Auswahlbox
   
   #Personenobjekt erstellen
   current_person = person.Person(find_person_data_by_name(current_user))

     
   #Bild der Person anzeigen
   image = Image.open(current_person.picture_path)
   
  
   st.write("currently selected user is: "+ current_user)
   st.write("age of current user: " + str(current_person.get_age()))
   st.write ("max heartrate calculated by age is: "+ str(current_person.calc_max_hr()))

   if current_person:
      test_dict = EKGdata.load_by_id(person_data, current_person.id)
      ekg = EKGdata(test_dict)
      ekg.find_peaks()
      ekg.plot_time_series()
      st.plotly_chart(ekg.fig)
      hr = ekg.estimate_hr_peaks()

      #st.write(f"Estimated Heart Rate: {hr.mean():.2f} bpm")
      
      ekg.make_plot_hr()
      st.plotly_chart(ekg.fig_hr)
      

with col2:
   st.header("Bild")
   st.image(image, caption=current_user)