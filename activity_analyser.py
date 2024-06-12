import pandas as pd
import plotly.graph_objects as go

def plot_performance_and_heart_rate(file_path):
    # Laden der Daten aus der angegebenen CSV-Datei in einem DataFrame
    df = pd.read_csv(file_path)

    # Ermitteln des Mittelwerts der Leistung
    average_performance = df['PowerOriginal'].mean()
    print("Mittelwert der Leistung:", average_performance)

    # Ermitteln des Maximalwerts der Leistung
    max_performance = df['PowerOriginal'].max()
    print("Maximalwert der Leistung:", max_performance)

    # Anzeigen der ersten paar Zeilen des DataFrames
    print(df.head())

    # Hinzufügen einer Spalte für die Zeit, falls sie nicht bereits vorhanden ist
    df["time"] = df.index

    # Erstellen der Plotly-Figur
    fig = go.Figure()

    # Hinzufügen der Leistung zum Plot
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['PowerOriginal'],
        name='Leistung (Watt)',
        yaxis='y1',
        line=dict(color='blue')
    ))

    # Hinzufügen der Herzfrequenz zum Plot
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['HeartRate'],
        name='Herzfrequenz (BPM)',
        yaxis='y2',
        line=dict(color='red')
    ))

    # Update der Layout-Parameter für zwei Y-Achsen
    fig.update_layout(
        title='Leistung und Herzfrequenz über die Zeit',
        xaxis_title='Zeit in s',
        yaxis=dict(
            title='Leistung (Watt)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Herzfrequenz (BPM)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=0.98,  # X-Position der Legende (0.0 bis 1.0)
            y=0.01,  # Y-Position der Legende (0.0 bis 1.0)
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return fig