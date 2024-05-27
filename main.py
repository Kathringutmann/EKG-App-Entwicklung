# Speichere diese Datei als main.py

import streamlit as st
from powercurve import calculate_power_curve
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("Leistungskurve Berechnung")

    # Pfadeinstellungen
    csv_file_path = "activity.csv"

    data = pd.read_csv(csv_file_path)
    st.write("Datenvorschau:", data.head())

    if 'PowerOriginal' in data.columns:
        power_data = data['PowerOriginal']

        duration = st.number_input("Gib die Dauer (in Sekunden) ein", min_value=1, value=1)

        df_power_curve = calculate_power_curve(power_data, duration)

        st.write("Leistungskurve:", df_power_curve.head())

        fig, ax = plt.subplots()
        ax.plot(df_power_curve['Time (s)'], df_power_curve['Power (W)'], label='Power Curve')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Power (W)')
        ax.set_title('Leistungskurve')
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Die CSV-Datei enthält keine 'PowerOriginal'-Spalte.")

if __name__ == "__main__":
    main()
