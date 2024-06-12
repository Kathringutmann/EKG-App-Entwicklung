import pandas as pd
import plotly.express as px

def read_my_csv(file_path):
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv(file_path, sep="\t", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Messwerte in mV", "Zeit in ms"]
    
    # Gibt den geladenen Dataframe zurück
    return df

def make_plot(df):
    # Erstellt einen Line Plot der ersten 2000 Werte mit der Zeit auf der x-Achse
    fig = px.line(df.head(2000), x="Zeit in ms", y="Messwerte in mV")
    return fig

# Dateipfad zur CSV-Datei
file_path = r'C:\Programmierübungen_II\EKG-App-Entwicklung\data\activity.csv'

# Einlesen der CSV-Datei und Erstellen des Plots
df = read_my_csv(file_path)
fig = make_plot(df)

# Anzeigen des Plots
fig.show()
