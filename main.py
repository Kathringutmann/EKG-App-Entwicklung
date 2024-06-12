import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person
from ekgdata import EKGdata
from PIL import Image
from power_data import load_data_for_plot, create_interactive_plot

# Benutzerdefinierte Funktion zur Synchronisierung des Slider- und Texteingabefeld-Werts
def sync_range_size():
    global range_size
    global range_size_input
    try:
        range_size = int(range_size_input)
    except ValueError:
        st.warning("Bitte geben Sie eine ganze Zahl ein.")
        range_size_input = str(range_size)

person_data = person.Person.load_person_data() #Personendaten laden
names = person.Person.get_person_list(person_data) #Namen der Personen in Liste speichern
    
current_person = None  #Variable für aktuelle Person
    
#Überschrift
st.title('EKG Analyse')

col1, col2 = st.columns(2) #Spalten erstellen

with col1:
    st.write("## Versuchsperson auswählen")
    current_user = st.selectbox('Versuchsperson', options=names, key="sbVersuchspersonen")
    current_person = person.Person(find_person_data_by_name(current_user))
    test_ids = person.Person.get_test_ids(current_person)
    image = Image.open(current_person.picture_path)
    st.write("Derzeit ausgewählter Nutzer ist: " + current_user)
    st.write("Alter des aktuellen Nutzers: " + str(current_person.get_age()))
    st.write("Max. Herzrate (basierend auf aktuellem Alter): " + str(current_person.calc_max_hr()))

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
    selected_test_id = st.selectbox('Wählen Sie eine Test-ID:', test_ids)
    st.write(f'Sie haben die Test-ID {selected_test_id} ausgewählt.')

    test_dict = EKGdata.load_by_id(person_data, selected_test_id)
    ekg = EKGdata(test_dict)
    ekg.find_peaks()
    ekg.plot_time_series()

    # Gesamtgröße des EKG-Datensatzes in ms (angenommen 600000 ms)
    total_size_ms = 600000

    # Slider zur Einstellung der Größe des ausgewählten Bereichs in ms
    range_size = st.slider("Ausschnittsgröße (ms)", 0, total_size_ms, 5000)

    # Texteingabefeld für präzise Eingabe der Ausschnittsgröße
    range_size_input = st.text_input("Ausschnittsgröße eingeben:", str(range_size))

    # Synchronisierung auslösen, wenn sich der Wert im Texteingabefeld ändert
    sync_range_size()

    # Synchronisierung auslösen, wenn sich der Wert des Sliders ändert
    if range_size != int(range_size_input):
        range_size_input = str(range_size)

    # Slider zur Verschiebung des ausgewählten Bereichs entlang des EKG-Grafiks in ms
    range_start = st.slider("Verschiebung (ms)", 0, total_size_ms - range_size, 0)

    # Bereichsende berechnen
    range_end = range_start + range_size

    # Anzeige der gewählten Bereiche
    st.write(f"Gewählter Bereich: {range_start} ms bis {range_end} ms")

    # Update plot with selected range
    ekg.update_axis(range_start, range_end)
    
    # Plot the updated figure
    st.plotly_chart(ekg.fig)


# Laden der Daten und Erstellen des Plots bei Auswahl einer Versuchsperson
if current_user is not None:
    df = load_data_for_plot(current_user)
    fig = create_interactive_plot(df)
    st.plotly_chart(fig)