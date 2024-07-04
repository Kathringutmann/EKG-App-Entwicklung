import json
import pandas as pd
import plotly.express as px
import scipy.signal as signal
from dtw import dtw
import numpy as np

class EKGdata:
    @staticmethod
    def load_by_id(person_data, id):
        """ Eine Funktion zum Laden eines EKG-Tests anhand der ID aus den Personendaten und gibt den Test zurück."""
        for person in person_data:
            for test in person["ekg_tests"]:
                if test["id"] == id:
                    return test
        return {}  # wenn keine ID gefunden wird, wird ein leeres Dictionary zurückgegeben

    def __init__(self, ekg_dict):
        """ Initialisiert ein EKG-Objekt mit den Daten aus dem übergebenen Dictionary."""
        self.id = ekg_dict["id"]  # ID des EKG-Tests
        self.date = ekg_dict["date"]  # Datum des EKG-Tests
        self.data = ekg_dict["result_link"]  # Link zur Datei mit den EKG-Daten
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])  # DataFrame erstellen
        self.df['Zeit in ms'] = self.df['Zeit in ms'] - self.df['Zeit in ms'].min()  # Zeit in ms relativ zum Start setzen

    def find_peaks(self):
        """ Findet die Peaks in den EKG-Daten und markiert sie im DataFrame."""
        x = self.df["Messwerte in mV"]
        self.peaks = signal.find_peaks(x, height=340)  # finde Peaks in den EKG-Daten
        self.df["Peak"] = False  # Peak-Spalte im DataFrame erstellen und auf False setzen
        self.df.loc[self.peaks[0], "Peak"] = True  # Peaks im DataFrame markieren
        return self.peaks  # Peaks zurückgeben

    def get_peaks_df(self):
        """ Gibt einen neuen DataFrame zurück, der nur die Peaks enthält."""
        return self.df.iloc[self.peaks[0]]  # DataFrame mit den Peaks zurückgeben
    def get_peaks_df(self):
        """Gibt einen neuen DataFrame zurück, der nur die Peaks enthält."""
        peaks_df = self.df.iloc[self.peaks[0]]  # Peaks aus dem DataFrame extrahieren
        peaks_df['ID'] = range(1, len(peaks_df) + 1)  # Spalte mit IDs hinzufügen
        return peaks_df  # DataFrame mit Peaks und IDs zurückgeben



    def plot_time_series(self):
        """ Erstellt einen interaktiven Plot der EKG-Daten und gibt ihn zurück."""
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV",
                           range_x=[100, 110],
                           range_y=[self.df["Messwerte in mV"].min(), self.df["Messwerte in mV"].max()])  # Plot erstellen, Achsen definieren
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='red', size=8), name='Peaks')  # Peaks hinzufügen
        self.fig.update_yaxes(range=[self.df["Messwerte in mV"].min(), self.df["Messwerte in mV"].max()])
        self.fig.update_xaxes(range=[self.df["Zeit in ms"].min(), self.df["Zeit in ms"].max()])
        return self.fig  # Plot zurückgeben

    def update_axis(self, range_start, range_end):
        """ Aktualisiert die x-Achsen des Plots mit den übergebenen Werten."""
        self.fig.update_xaxes(range=[range_start, range_end])

    def estimate_hr_peaks(self):
        """ Schätzt die Herzfrequenz aus den Peaks und gibt sie zurück."""
        rr_intervall = self.get_peaks_df()["Zeit in ms"].diff()  # Zeitdifferenz zwischen den Peaks in ms
        self.hr = 1 / rr_intervall  # Herzfrequenz berechnen
        return self.hr  # Herzfrequenz zurückgeben

    def make_plot_hr(self):
        """ Erstellt einen interaktiven Plot der Herzfrequenz und gibt ihn zurück."""
        peaks_df = self.get_peaks_df().iloc[1:]  # ersten Wert entfernen, da er nicht relevant ist
        self.fig_hr = px.line(x=self.get_peaks_df()["Zeit in ms"], y=self.hr, title='Heart Rate Over Time', labels={'x': 'Time (ms)', 'y': 'Heart Rate (bpm)'})  # Plot erstellen
        return self.fig_hr

    def heartbeat_deviation(self, beat1: int, beat2: int):
        """ Berechnet die Abweichungen zwischen zwei Herzschlägen und gibt sie zurück."""
        df_beat1 = self.df[self.df["Beat"] == 1]  # DataFrame für den ersten Herzschlag
        return 1.1  # float

    def heartbeat_determine(self):
        """ Bestimmt die Herzschläge und fügt sie dem durchnummerierten DataFrame hinzu."""
        self.df["Beat"] = 0  # Initialisiere eine neue Spalte 'Beat' mit 0
        self.df['Peak Group'] = pd.NA  # Initialisiere eine neue Spalte 'Peak Group' mit NaN
        counter = 0  # Zähler für die Peak-Gruppen
        for i, row in self.df.iterrows():  # Durch die Zeilen des DataFrame iterieren und die Peak-Gruppen zuweisen
            if row['Peak']:
                counter += 1
            self.df.at[i, 'Peak Group'] = counter
        print(self.df)

    def plot_heartbeat(self, number):
        """ Plottet den Herzschlag mit der angegebenen Nummer und gibt ihn zurück."""
        df_filtered = self.df[self.df['Peak Group'] == number]  # Filtern des DataFrames für den gewünschten Herzschlag
        fig = px.line(df_filtered, x='Zeit in ms', y='Messwerte in mV', title=f'Herzschlag Nummer {number}', markers=True)  # Plotten des Herzschlags mit Plotly
        fig.update_layout(xaxis_title='Zeit in ms', yaxis_title='Messwerte in mV', template='plotly_white')
        fig.show()
        return fig

    def heartbeat_avg(self, resample_length=100):
        """ Berechnet den durchschnittlichen Herzschlag und gibt ihn zurück."""
        # Extrahiere alle Herzschläge in eine Liste
        heartbeats = []
        for group in self.df['Peak Group'].unique():
            df_group = self.df[self.df['Peak Group'] == group]
            heartbeats.append(df_group['Messwerte in mV'].values)
        
        # Verwende den ersten Herzschlag als Referenz
        reference = heartbeats[0]
        
        # Warpe alle Herzschläge zur Referenz und berechne den Durchschnitt
        aligned_heartbeats = []
        
        for heartbeat in heartbeats:
            alignment = dtw(heartbeat, reference, keep_internals=True)
            aligned_heartbeat = [heartbeat[idx] for idx in alignment.index1]
            aligned_heartbeats.append(aligned_heartbeat)
        
        # Berechne den Durchschnitt über alle gewarpten Herzschläge hinweg
        resampled_heartbeats = []
        for heartbeat in aligned_heartbeats:
            resampled_heartbeat = np.interp(np.linspace(0, len(heartbeat) - 1, resample_length), np.arange(len(heartbeat)), heartbeat)
            resampled_heartbeats.append(resampled_heartbeat)
        
        # Berechne den Durchschnitt über alle resampled Herzschläge hinweg
        avg_heartbeat = np.mean(resampled_heartbeats, axis=0)
        
        # Erstellen eines DataFrames für den durchschnittlichen Herzschlag
        self.avg_df = pd.DataFrame({
            'Zeit in ms': np.linspace(self.df['Zeit in ms'].min(), self.df['Zeit in ms'].max(), len(avg_heartbeat)),
            'Durchschnitt Herzschlag': avg_heartbeat
        })
        
        return self.avg_df


    def plot_avg_hb(self):
        """ Plottet den durchschnittlichen Herzschlag und gibt ihn zurück."""
        fig = px.line(self.avg_df, x='Zeit in ms', y='Durchschnitt Herzschlag', title='Durchschnittlicher Herzschlag')
        fig.update_layout(xaxis_title='Zeit in ms', yaxis_title='Messwerte in mV', template='plotly_white')
        fig.show()

    #def heartbeat_comparison(self, ekg_data, heartbeat_id , threshold=0.1):
    def warp_heartbeat(heartbeat, reference):
        """Warpt einen Herzschlag auf die Referenzlänge."""
        alignment = dtw(heartbeat, reference, keep_internals=True)
        warped_heartbeat = [heartbeat[idx] for idx in alignment.index1]
        return warped_heartbeat

    def resample_heartbeat(heartbeat, resample_length):
        """Resamplet einen Herzschlag auf die gewünschte Länge."""
        resampled_heartbeat = np.interp(np.linspace(0, len(heartbeat) - 1, resample_length), np.arange(len(heartbeat)), heartbeat)
        return resampled_heartbeat
    
    def calculate_mse(array1, array2):
        """Berechnet den mittleren quadratischen Fehler (MSE) zwischen zwei Arrays."""
        mse = np.mean((array1 - array2)**2)
        return mse

    sorted_mse_values, sorted_indices = zip(*sorted(zip(mse_values, range(len(mse_values)))))
    
top_5_indices = sorted_indices[:5]  # Identifiziere die Indizes der Top 5 MSE-Werte
top_5_deviations = [warped_heartbeats_array[i] - avg_heartbeat for i in top_5_indices]  # Berechne die Abweichungen




# Testen der Klasse
if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data, 2) 
    ekg = EKGdata(test_dict)
    
    # Find peaks and determine heartbeats
    ekg.find_peaks()
    ekg.heartbeat_determine()
    
    # Calculate average heartbeat and plot it
    avg_hs = ekg.heartbeat_avg()
    ekg.plot_avg_hb()
    
    # Importieren Sie die EKGdata-Klasse (falls noch nicht geschehen)
    from ekgdata import EKGdata

    # Angenommen, Sie haben ein EKGdata-Objekt namens "ekg_data" erstellt
    ekg = EKGdata(test_dict)

    # Rufen Sie die "heartbeat_comparison"-Funktion auf und speichern Sie die Ergebnisse in Variablen
    riskiest_heartbeats, avg_heartbeat, avg_heartbeat_plot = ekg.heartbeat_comparison(ekg, heartbeat_id=100, threshold=0.1)
    

    # Verarbeiten und visualisieren Sie die Ergebnisse (optional)
    
    print("Riskiest heartbeats:")
    for heartbeat_id, mse, fig in riskiest_heartbeats:
        print(f"Heartbeat ID: {heartbeat_id}, Deviation: {mse}")
        fig.show()  # Display the comparison plot

    for heartbeat, mse, fig in riskiest_heartbeats:
        print(f"Herzschlag-ID: {heartbeat}, Abweichung: {mse}")
    fig.show()  # Plot des Vergleichs anzeigen

    print("Durchschnittlicher Herzschlag:")
    avg_heartbeat_plot.show()  # Plot des durchschnittlichen Herzschlags anzeigen
    
    
