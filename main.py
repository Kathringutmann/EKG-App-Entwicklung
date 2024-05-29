import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import powercurve
import leistungsverlauf



st.title('Power Curve Analysis')

# Fester Pfad zur CSV-Datei
file_path = r'C:\Programmierübungen_II\EKG-App-Entwicklung\activity.csv'

# Daten laden
df = leistungsverlauf.load_csv(file_path)

# Daten normalisieren
normalized_df = leistungsverlauf.normalize_data(df)

# Normalisierte Daten anzeigen
st.subheader('Normalized Data')
st.write(normalized_df)

# Power-Curve Diagramm anzeigen
st.subheader('Power Curve')
fig = leistungsverlauf.plot_power_curve(normalized_df)
st.pyplot(fig)



# Daten laden
df = powercurve.load_csv(file_path)

# Daten plotten
power_curve_df = powercurve.compute_powercurve(df)
fig = powercurve.plot_data(power_curve_df)
st.pyplot(fig)


#print(find_duration_powerlevel (df, 250))
#print(compute_powercurve (df))
