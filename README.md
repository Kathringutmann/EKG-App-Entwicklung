# CardioGraph 📈
*YOUR HEART, OUR PRIORITY*
![Logo1](logo_1.png)

## Einführung
Willkommen bei CardioGraph! Diese benutzerfreundliche, Streamlit-basierte Webanwendung wurde entwickelt, um Ihnen die Analyse und Visualisierung von EKG-Daten zu erleichtern. CardioGraph ermöglicht Ihnen EKG-Daten zu untersuchen, Herzaktivitäten zu analysieren und wertvolle Einblicke in die Herzgesundheit zu gewinnen.

## Zielgruppe
Diese Anwendung richtet sich an:
- **medizinische Fachkräfte:** zur klinischen Diagnostik und Überwachung der Herzgesundheit.
- **Forscher im Bereich Kardiologie:** zur Analyse großer Datensätze und Identifikation von Mustern.
- **Sportwissenschaftler:** zur Überwachung der Herzaktivität von Athleten und Analyse der Trainingseffekte.

## Funktionen der Anwendung

### Wilkommensseite
- **Begrüßungstext und Bild:** Eine freundliche Einführung in die Anwendung.
- **Button "Jetzt Starten"**: Doppelklicken Sie auf diesen Button, um zur Analyse-Seite zu gelangen.

### EKG-Analyse-Seite
#### Sidebar
- **Versuchsperson auswählen:**
  Wählen Sie eine Versuchsperson aus der Dropdown-Liste.
- **Bild und Informationen:**
  Anzeigen eines Bildes und grundlegender Informationen (Alter, maximale Herzfrequenz) der ausgewählten Versuchsperson.
- **Test-ID auswählen:**
  Wählen Sie eine Test-ID, um die entsprechenden EKG-Daten zu laden.

#### Tab1: EKG-Daten
- **EKG-Daten anzeigen:**
  Plot des gesamten EKG-Datensatzes der ausgewählten Test-ID, der die Herzaktivität über die Zeit zeigt. 
- **Herzfrequenz schätzen:**
  Erkennung von Peaks in den EKG-Daten zur Schätzung der Herzfrequenz, dargestellt in einem separaten Plot.
- **Ausschnittsgröße anpassen:**
  Passen Sie die Größe des angezeigten EKG-Ausschnitts mittels Slider oder Eingabe einer genauen Zahl an.
- **Bereich verschieben:**
  Verschieben Sie den angezeigten Bereich entlang der EKG-Grafik zur Untersuchung verschiedener Datenteile.

#### Tab 2: Leistungsdaten
- **Leistungsdaten visualisieren:**
  Laden und Visualisieren der Leistungsdaten der ausgewählten Versuchsperson.

#### Tab 3: Herzschlaganalyse
- **Durchschnittlicher Herzschlag:**
  Der durchschnittliche Herzschlag wird berechnet und geplottet.
- **Vergleich der Herzschläge mit dem Durchschnitt:**
  Die Herzschläge werden mit dem durchschnittlichen Herzschlag verglichen und die Ergebnisse werden angezeigt.

## Zugang zur Anwendung
Sie können direkt auf die Webanwendung zugreifen indem Sie die folgende URL besuchen:
```ruby
https://ekg-app-entwicklung-kg-eg-ga.streamlit.app/
```

## Installation & Nutzung
1. Klonen Sie das Repository:
```ruby
git clone https://github.com/IhrBenutzername/ekg-analyse-app.git
```

3. mit folgendem Befehl können Sie die benötigten Bibliotheken installieren:
```ruby
pip install -r requirements.txt
```

4. Starten Sie die App mit folgendem Befehl:
```ruby
streamlit run main.py
```
## benötigte Bibliotheken
- pandas
- streamlit
- PIL
- scipy
- plotly
- json
- signal
- dtw
- numpy


## Dateien
- main.py: Hauptdatei der Anwendung.
- read_data.py: Skript zum Einlesen der Personendaten.
- person.py: Modul zur Verwaltung der Personendaten.
- ekgdata.py: Modul zur Verarbeitung und Visualisierung der EKG-Daten.
- data/person_db.json: Beispielhafte JSON-Datei mit den Personendaten.
- activity_analyse.py: Interaktiver Plot zur Leistung über die Zeit.
- dataframe_plot.py: Modul zur Erstellung von Plots aus DataFrames.
- power_data.py: Modul zur Verarbeitung von Leistungsdaten.
- requirements.txt: Liste der benötigten Bibliotheken.
- test_5_Schläge.py: Skript zum Testen der Erkennung von fünf Herschlägen.

## Beispiel
Hier ist ein Beispiel - Screenshot der Anwendung in Aktion:
Beispiel Person: Huber, Julian
![Screenshot1](screenshot_1.png)
![Screenshot12](screenshot_12.jpeg)
![Screenshot2](screenshot_2.png)
![Screenshot3](screenshot_3.png)


## Gewünschte Erweiterung/gewünschtes Ziel:
Durchschnitts Herzschlag mit allen anderen Herzschlägen vergleichen und die 5 abweichendsten anzeigen:
-> nächste schritte in ekg.py bei zeile 163 bei funktion herzschlag_vergleich eintragen:

1. mit dtw alle auf eine länge wieder bringen, da man nur so vergleichen kann Bsp.:
        Verwende den ersten Herzschlag als Referenz
        referenz = herzschlaege[0]
        
        # Warpe alle Herzschläge zur Referenz und speichere die gewarpten Herzschläge
        aligned_herzschlaege = []
        
        for herzschlag in herzschlaege:
            alignment = dtw(herzschlag, referenz, keep_internals=True, dist_method=dist_metric)
            aligned_herzschlag = [herzschlag[idx] for idx in alignment.index1]
            aligned_herzschlaege.append(aligned_herzschlag)
        
2. und dann resampel Bsp.:
        # Resample the aligned heartbeats to a common length
        resampled_herzschlaege = []
        for herzschlag in aligned_herzschlaege:
            resampled_herzschlag = np.interp(np.linspace(0, len(herzschlag) - 1, resample_length), np.arange(len(herzschlag)), herzschlag)
            resampled_herzschlaege.append(resampled_herzschlag)
        
        # Berechne den Durchschnitt über alle resampled Herzschläge hinweg
        avg_herzschlag = np.mean(resampled_herzschlaege, axis=0)

3. dann in der formel mean square error MSE in arrays
        (2 arrays mit gleicher länge!)
        Formel:(array 1 - array2)**2 = MSE

4. durch Formel hat man einen Array? ------ NACHFRAGEN!!!!
        -> aus diesen einzelnen Datenpunkten-differenzen, können dann die 5 größten Abweichungen gefiltert werden
        ? : eventuell könnten mehr als 5 Abweichungen gefiltert werden müssen, damit man die 5 Herzschläge mit den größten Abweichungen bekommt

        -> diese jeweils einzeln mit plotly ausplotten


## Probleme mit der Erweiterung


## Endergebnis


## Feedback 🗣️ & Kontaktinformationen
Falls Sie Probleme beim Installieren oder Verwenden der Anwendung haben oder Verbesserungsvorschläge haben, zögeren Sie nicht, ein Issue im Repository zu öffnen oder eine E-Mail an das Entwicklerteam unter : ag9716@mci4me.at, gk2575@mci4me.at oder ge7045@mci4me.at zu senden.



Wir hoffen, dass CardioGraph Ihnen dabei hilft, tiefere Einblicke in die Herzgesundheit zu gewinnen und eine wertvolle Ressource für Ihre medizinischen, sportlichen oder wissenschaftlichen Analysen darstellt.

***Viel Spaß beim Erkunden und Analysieren Ihrer EKG-Daten mit CardioGraph!🦾 💻 📈***
