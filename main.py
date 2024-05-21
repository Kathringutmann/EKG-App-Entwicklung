import streamlit as st
from read_data import get_name, get_person_data, find_person_data_by_name
import plotly.graph_objects as go
import pandas as pd

person_data = get_person_data()
names = get_name(person_data)

# Laden der Daten für den Plot
def load_data_for_plot(person_name):
    person_data = find_person_data_by_name(person_name)
    file_path = person_data["ekg_tests"][0]["data_path"]
    df = pd.read_csv(file_path)
    return df

# Funktion zum Erstellen des interaktiven Plots mit Plotly
def create_interactive_plot(df):
    df["time"] = df.index
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['PowerOriginal'], name='Leistung (Watt)', yaxis='y1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['time'], y=df['HeartRate'], name='Herzfrequenz (BPM)', yaxis='y2', line=dict(color='red')))
    fig.update_layout(title='Leistung und Herzfrequenz über die Zeit', xaxis_title='Zeit in s',
                      yaxis=dict(title='Leistung (Watt)', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
                      yaxis2=dict(title='Herzfrequenz (BPM)', titlefont=dict(color='red'), tickfont=dict(color='red'),
                                  overlaying='y', side='right'),
                      legend=dict(x=0.1, y=0.9, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'))
    return fig

# Überschrift
st.title('EKG Analyse')

from PIL import Image

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")  # Unterüberschrift
    current_user = st.selectbox('Versuchsperson', options=names, key="sbVersuchspersonen")  # Auswahlbox
    image = Image.open(find_person_data_by_name(current_user)["picture_path"])
    st.write("Currently selected user is: " + current_user)

with col2:
    st.header("Bild")
    st.image(image, caption=current_user)

# Laden der Daten und Erstellen des Plots bei Auswahl einer Versuchsperson
if current_user is not None:
    df = load_data_for_plot(current_user)
    fig = create_interactive_plot(df)
    st.plotly_chart(fig)
