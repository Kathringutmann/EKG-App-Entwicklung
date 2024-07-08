# Ziel der Anwendung
Die Anwendung ermöglicht die Analyse von EKG-Daten, indem sie dem Benutzer erlaubt, Versuchspersonen auszuwählen und spezifische Ausschnitte ihrer EKG-Daten visuell zu untersuchen.
Ziel ist es, eine benutzerfreundliche Oberfläche zur Analyse und Visualisierung von EKG-Daten bereitzustellen, um Einblicke in die Herzaktivität der Versuchspersonen zu gewinnen.

## Funktionen der Anwendung
### Versuchsperson auswählen: 
Eine Versuchsperson kann aus der Dropdown-Liste auf der linken Seite ausgewählt werden.
### Bild und Informationen: 
Ein Bild der ausgewählten Versuchsperson sowie einige grundlegende Informationen wie Alter und maximal berechnete Herzfrequenz werden angezeigt.
### Test-ID auswählen: 
Man wählt eine Test-ID aus der Dropdown-Liste, um die entsprechenden EKG-Daten zu laden.
### EKG-Daten anzeigen: 
Die EKG-Daten der ausgewählten Test-ID werden als Plot dargestellt, der die Herzaktivität über die Zeit zeigt.
### Herzfrequenz schätzen:
Peaks in den EKG-Daten werden erkannt und zur Schätzung der Herzfrequenz verwendet. Diese Herzfrequenz wird ebenfalls als Plot dargestellt.
### Ausschnittsgröße anpassen: 
Man kann die Größe des angezeigten EKG-Ausschnitts mit einem Slider oder durch Eingabe einer genauen Zahl anzeigen lassen.
### Bereich verschieben: 
Man kann den angezeigten Bereich entlang der EKG-Grafik verschieben, um verschiedene Teile der Daten zu sehen.

# Installation & Nutzung
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
### benötigte Bibliotheken
- pandas
- streamlit
- PIL
- scipy
- plotly
- json
- signal
- dtw
- numpy


### Dateien
- main.py: Hauptdatei der Anwendung.
- read_data.py: Skript zum Einlesen der Personendaten.
- person.py: Modul zur Verwaltung der Personendaten.
- ekgdata.py: Modul zur Verarbeitung und Visualisierung der EKG-Daten.
- data/person_db.json: Beispielhafte JSON-Datei mit den Personendaten.
- activity_analyse.py: Interaktiver Plot zur Leistung über die Zeit.
- dataframe_plot.py:
- power_data.py: 
- requirements.txt:
- test_5_Schläge.py:  

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
