import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import person
from ekgdata import EKGdata
import ekgdata
from PIL import Image
from power_data import load_data_for_plot, create_interactive_plot

# Definiere die Hintergrundfarbe für die gesamte App
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C6EFFD; /* Light blue background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Funktion für die Willkommensseite
def welcome_page():
    st.markdown("<h1 style='text-align: center;'>Willkommen zu CardioGraph!</h1>", unsafe_allow_html=True)
    
    # Spalten erstellen (verhältnismäßige Breite: 1/4 - 1/2 - 1/4)
    left_column, middle_column, right_column = st.columns([1, 2, 1])

# Fülle die mittlere Spalte mit dem Bild
    with middle_column:
        image = st.image("CardioGraph-Logo.png", use_column_width=True)

    
    
    
    # Zentriere den Button horizontal
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button('Jetzt starten'):
            st.session_state.page = 'analysis'

# Funktion für die EKG-Analyse-Seite
def ekg_analysis_page():
    person_data = person.Person.load_person_data()  # Personendaten laden
    names = person.Person.get_person_list(person_data)  # Namen der Personen in Liste speichern

    # Sidebar erstellen
    st.sidebar.title('Daten zur Person')

    current_user = st.sidebar.selectbox('**Nutzer/in auswählen:**', options=names, key="sbVersuchspersonen")
    current_person = person.Person(find_person_data_by_name(current_user))
    test_ids = person.Person.get_test_ids(current_person)
    image = Image.open(current_person.picture_path)
    st.sidebar.write("Alter: " + str(current_person.get_age()) + " Jahre")
    st.sidebar.image(image, caption=current_user)
    selected_test_id = st.sidebar.selectbox('Test-ID auswählen:', test_ids)
    st.sidebar.write("Maximale Herzrate: " + str(current_person.calc_max_hr()))
    st.sidebar.write("Testdatum:", EKGdata.load_by_id(person_data, selected_test_id)["date"])

    # Überschrift
    st.title('CardioGraph')

    tab1, tab2, tab3 = st.tabs(["EKG Data", "Power Data", "Heart-Rate Analysis"])  # Tabs erstellen

    with tab1:
        if current_person:
            test_dict = EKGdata.load_by_id(person_data, current_person.id)
            ekg = EKGdata(test_dict)
            ekg.find_peaks()
            ekg.plot_time_series()  # Herzfrequnzanalyse
            st.plotly_chart(ekg.fig)  # Peaks finden
            hr = ekg.estimate_hr_peaks()

        test_dict = EKGdata.load_by_id(person_data, selected_test_id)
        ekg = EKGdata(test_dict)
        ekg.find_peaks()
        ekg.plot_time_series()

        # Gesamtgröße des EKG-Datensatzes in ms (angenommen 600000 ms)
        total_size_ms = 600000

        # Slider zur Einstellung der Größe des ausgewählten Bereichs in ms
        range_size = st.slider("Ausschnittsgröße (ms)", 0, total_size_ms, 5000, key="range_size")

        # Texteingabefeld für präzise Eingabe der Ausschnittsgröße
        range_size_input = st.text_input("Ausschnittsgröße eingeben:", str(range_size), key="range_size_input")

        try:
            range_size = int(range_size_input)
        except ValueError:
            st.warning("Bitte geben Sie eine ganze Zahl ein.")
            range_size = 5000

        # Slider zur Verschiebung des ausgewählten Bereichs entlang des EKG-Grafiks in ms
        range_start = st.slider("Verschiebung (ms)", 0, total_size_ms - range_size, 0, key="range_start")

        # Bereichsende berechnen
        range_end = range_start + range_size

        # Anzeige der gewählten Bereiche
        st.write(f"Gewählter Bereich: {range_start} ms bis {range_end} ms")

        # Update plot with selected range
        ekg.update_axis(range_start, range_end)
        
        # Plot the updated figure
        st.plotly_chart(ekg.fig)

        # Herzfrequenzanalyse
        hr = ekg.estimate_hr_peaks()  
        ekg.make_plot_hr()
        st.plotly_chart(ekg.fig_hr)

    with tab2:
        # Laden der Daten und Erstellen des Plots bei Auswahl einer Versuchsperson
        if current_user is not None:
            df = load_data_for_plot(current_user)
            fig = create_interactive_plot(df)
            st.plotly_chart(fig)

    with tab3:  # Tab 3 für Erweiterung der Herzfrequenzanalyse
        st.write("## Herzfrequenzanalyse")
        st.write("Erweiterung hinzufügen!!!")

# Initialisiere den Session State für die Seitenwahl
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# Logik zur Anzeige der richtigen Seite basierend auf dem Session State
if st.session_state.page == 'welcome':
    welcome_page()
else:
    ekg_analysis_page()
