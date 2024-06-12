
import plotly.graph_objects as go
import pandas as pd

from read_data import find_person_data_by_name
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