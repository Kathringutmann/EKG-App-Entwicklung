import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person
import ekgdata
from PIL import Image

person_data = person.Person.load_person_data()
names = person.Person.get_person_list(person_data)
current_person = None

st.title('EKG Analyse')

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    current_user = st.selectbox('Versuchsperson', options=names, key="sbVersuchspersonen")
    current_person = person.Person(find_person_data_by_name(current_user))
    test_ids = person.Person.get_test_ids(current_person)
    image = Image.open(current_person.picture_path)
    st.write("currently selected user is: " + current_user)
    st.write("age of current user: " + str(current_person.get_age()))
    st.write("max heartrate calculated by age is: " + str(current_person.calc_max_hr()))

with col2:
    st.header("Bild")
    st.image(image, caption=current_user)
    selected_test_id = st.selectbox('Wählen Sie eine Test-ID:', test_ids)
    st.write(f'Sie haben die Test-ID {selected_test_id} ausgewählt.')

    test_dict = ekgdata.EKGdata.load_by_id(person_data, selected_test_id)
    ekg = ekgdata.EKGdata(test_dict)
    ekg.find_peaks()
    ekg.make_plot()

    # Gesamtgröße des EKG-Datensatzes in ms (angenommen 600000 ms)
    total_size_ms = 600000

    # Slider zur Einstellung der Größe des ausgewählten Bereichs in ms
    range_size = st.slider("Ausschnittsgröße (ms)", 1000, total_size_ms, 5000)

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
