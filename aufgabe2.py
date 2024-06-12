import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Funktion zur Unterteilung der Herzfrequenz in Zonen
def get_heart_rate_zones(df, max_hr):
    zones = {
        'Zone 1': (0.0, 0.6 * max_hr),
        'Zone 2': (0.6 * max_hr, 0.7 * max_hr),
        'Zone 3': (0.7 * max_hr, 0.8 * max_hr),
        'Zone 4': (0.8 * max_hr, 0.9 * max_hr),
        'Zone 5': (0.9 * max_hr, max_hr)
    }
    df['Zone'] = pd.cut(df['HeartRate'], bins=[0, 0.6 * max_hr, 0.7 * max_hr, 0.8 * max_hr, 0.9 * max_hr, max_hr],
                        labels=['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5'], right=False)
    return df, zones

# Funktion zur Erstellung des interaktiven Plots
def create_interactive_plot(df, zones):
    fig = go.Figure()
    df["time"] = df.index
    
    # Hinzufügen der Herzfrequenz zum Plot
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['HeartRate'],
        name='Herzfrequenz (BPM)',
        yaxis='y1',
        line=dict(color='red')
    ))
    
    # Hinzufügen der Leistung zum Plot
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['PowerOriginal'],
        name='Leistung (Watt)',
        yaxis='y2',
        line=dict(color='blue')
    ))

    # Farben für die Zonen
    colors = ["green", "yellow", "orange", "coral", "purple"]
    
    # Hinzufügen der farbigen Bereiche für die Herzfrequenzzonen
    for i, (zone, (y0, y1)) in enumerate(zones.items()):
        fig.add_hrect(
            y0=y0,
            y1=y1,
            fillcolor=colors[i],
            opacity=0.2,
            line_width=0,
            yref="y"
        )
    
    # Update der Layout-Parameter für zwei Y-Achsen
    fig.update_layout(
        title='Leistung und Herzfrequenz über die Zeit',
        xaxis_title='Zeit in s',
        yaxis=dict(
            title='Herzfrequenz (BPM)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red')
        ),
        yaxis2=dict(
            title='Leistung (Watt)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=1,  # X-Position der Legende (0.0 bis 1.0)
            y=0,  # Y-Position der Legende (0.0 bis 1.0)
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )
    
    return fig

# Laden der CSV-Datei
df = pd.read_csv("data/activity.csv")

# Benutzerdefinierte Eingabe für die maximale Herzfrequenz
max_hr = st.number_input('Maximale Herzfrequenz (BPM):', min_value=100, max_value=220, value=200)

# Berechnung des Mittelwerts und des Maximalwerts der Leistung
average_performance = df['PowerOriginal'].mean()
max_performance = df['PowerOriginal'].max()

# Überschrift für die gesamte Analyse
st.markdown("<h1 style='text-align: center; color: #D2691E;'>EKG Analyse</h1>", unsafe_allow_html=True)

# Anzeigen des Mittelwerts und des Maximalwerts der Leistung
st.markdown(f"**Mittelwert der Leistung:** {average_performance:.2f} Watt")
st.markdown(f"**Maximalwert der Leistung:** {max_performance:.2f} Watt")

# Unterteilen der Herzfrequenz in Zonen
df, zones = get_heart_rate_zones(df, max_hr)

# Berechnung der Zeit in jeder Zone und der durchschnittlichen Leistung in den Zonen
time_in_zones = df['Zone'].value_counts().sort_index()
average_power_in_zones = df.groupby('Zone')['PowerOriginal'].mean()

# Überschrift für die Analyse der Herzfrequenzzonen
st.markdown("<h2 style='text-align: center; color: #D2691E;'>Herzfrequenzzonen</h2>", unsafe_allow_html=True)

# Anzeigen der Zeit in den Herzfrequenzzonen
st.markdown("**Zeit in den Herzfrequenzzonen:**")
for zone, time in time_in_zones.items():
    st.write(f"{zone}: {time} Sekunden")

# Anzeigen der durchschnittlichen Leistung in den Herzfrequenzzonen
st.markdown("**Durchschnittliche Leistung in den Herzfrequenzzonen:**")
for zone, avg_power in average_power_in_zones.items():
    st.write(f"{zone}: {avg_power:.2f} Watt")

# Anzeigen des interaktiven Plots
st.markdown("<h2 style='text-align: center; color: #D2691E;'>Leistung und Herzfrequenz über die Zeit</h2>", unsafe_allow_html=True)
st.plotly_chart(create_interactive_plot(df, zones))
