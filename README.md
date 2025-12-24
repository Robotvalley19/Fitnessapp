# Fitness-App

Eine **lokale Fitness-App** zur Verwaltung von Fitnessprofilen, Gewicht, BMI, Trainingsfokus und Übungen.
Die App ist vollständig lokal und **browserbasiert**, speichert Daten in CSV-Dateien und benötigt keine externe Datenbank.

---

## Features

* **Profile erstellen und bearbeiten**: Name, Alter, Geschlecht, Größe, Start- und Zielgewicht.
* **Trainingsplanung**: Auswahl von Trainingstagen und Trainingsfokus (Ganzkörper, Arme, Oberkörper, Bauch/Rücken, Beine/Po, Joggen, Trampolin).
* **Gewichts- und BMI-Tracking**: Einfache Eingabe von Gewicht, automatische Berechnung von BMI und optionalen Kalorieninformationen.
* **Dynamische Anzeige von Übungen**: Übersichtliche Darstellung der Übungen, abhängig vom Trainingsfokus.
* **Interaktive Diagramme**: Verlauf von Gewicht und BMI visualisiert mit Chart.js.
* **Animierter Hightech-Hintergrund**: Modernes, animiertes Linienmuster auf jeder Seite für ein futuristisches UI-Erlebnis.
* **Lokale Datenspeicherung**: Alle Daten werden lokal in CSV-Dateien gespeichert (`profiles.csv` und `weight_history.csv`).

---

## Design & Fonts

Die App nutzt **lokale Fonts**, um Abmahnungen oder rechtliche Probleme zu vermeiden:

* **Roboto Mono Regular & Bold**

  * Schriftart für Überschriften, Buttons, Labels und Eingabefelder.
  * Die Fonts liegen lokal unter `static/fonts/RobotoMono-Regular.ttf` und `RobotoMono-Bold.ttf`.
  * Vorteil: die App funktioniert **offline** ohne Internetverbindung zu Google Fonts.

**CSS & Styling**:

* Moderne Farbpalette: dunkler Hintergrund (#0d0d0d) mit Akzentfarben (#00d1b2) für Buttons, Überschriften und Rahmen.
* Transparente Container mit `backdrop-filter: blur()` für Glas-Effekt.
* Responsive Layout für alle Bildschirmgrößen.
* Eingabefelder und Buttons mit Hover-Effekten für bessere Interaktivität.

---

## Installation & Setup auf Raspberry Pi 4

### 1. Repository klonen

```bash
git clone https://github.com/Robotvalley19/Fitnessapp.git
cd Fitnessapp
```

> Die App läuft problemlos auf einem **Raspberry Pi 4** und kann über ein zentrales Tablet im Haus abgerufen werden.

### 2. Python-Umgebung vorbereiten

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. App starten

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0
```

> Die App ist im Heimnetz über die IP des Raspberry Pi erreichbar, z. B. `http://192.168.178.42:5000` auf dem Tablet.

### 4. Automatischen Start beim Booten einrichten (optional)

```bash
sudo nano /etc/systemd/system/fitnessapp.service
```

Füge folgendes ein:

```ini
[Unit]
Description=Lokale Fitness-App
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Fitnessapp
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
ExecStart=/home/pi/Fitnessapp/venv/bin/flask run --host=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Service aktivieren:

```bash
sudo systemctl daemon-reload
sudo systemctl enable fitnessapp.service
sudo systemctl start fitnessapp.service
```

### 5. Lokale Datenspeicherung

* `profiles.csv`: Enthält Fitnessprofile.
* `weight_history.csv`: Enthält Gewicht und BMI-Verlauf.

> Alle Daten bleiben **lokal auf dem Pi**, keine Internetverbindung nötig.

---

## Nutzung über Tablet

* Tablet im Heimnetz öffnen und die IP des Raspberry Pi eingeben, z. B.:
  `http://192.168.178.42:5000`
* Die App kann als **zentrale Fitness-Station** im Haus genutzt werden.

---

## Lizenz

Die App ist **frei nutzbar und offline**, alle Fonts sind lokal eingebunden, keine externe Datenbank oder Cloud erforderlich.
