- venv Ordner erstellen: main.py -> rechts unten auf Zahlen -> in Suchleiste den Venv Ordner anklicken

- venv aktivieren, um in die Umgebung verschiedene Sachen installieren -> in Kommandozeile erscheint grünes Venv und dann kann man mit pip install ... das gewünschte installieren

- read_data.py : json datei-> Funktion, die datei einließt -> dictionary mit der Person erstellt -> Funktion: nur den Firstname extrahiert-> Einer leeren Liste werden die Namen übergeben -> Funktion die die namen anzeigt

- öffnen der Webseite: Im Terminal: streamlit run main.py 

-pip freeze > requirements.txt

# Ziel der Anwendung
Die Anwendung ermöglicht die Analyse von EKG-Daten, indem sie dem Benutzer erlaubt, Versuchspersonen auszuwählen und spezifische Ausschnitte ihrer EKG-Daten visuell zu untersuchen.



## Versuchsperson auswählen: 
Eine Versuchsperson kann aus der Dropdown-Liste auf der linken Seite ausgewählt werden.
## Bild und Informationen: 
Ein Bild der ausgewählten Versuchsperson sowie einige grundlegende Informationen werden angezeigt.
## Test-ID auswählen: 
Man wählt eine Test-ID aus der Dropdown-Liste, um die entsprechenden EKG-Daten zu laden.
## EKG-Daten anzeigen: 
Die EKG-Daten der ausgewählten Test-ID werden als Plot dargestellt.
## Ausschnittsgröße anpassen: 
Man kann die Größe des angezeigten EKG-Ausschnitts mit einem Slider oder durch Eingabe einer genauen Zahl anzeigen lassen.
## Bereich verschieben: 
Man kann den angezeigten Bereich entlang der EKG-Grafik verschieben, um verschiedene Teile der Daten zu sehen.

# Ziel der Anwendung
Die Anwendung bietet eine benutzerfreundliche Oberfläche zur Analyse und Visualisierung von EKG-Daten, um Einblicke in die Herzaktivität der Versuchspersonen zu gewinnen.







