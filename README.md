# 🏋️ Fitness-App (Flask Web Application)

Eine vollständig lokale, browserbasierte Fitness-Webanwendung zur Verwaltung von Fitnessprofilen, Trainingsfokus, Gewicht, BMI und Kalorienverbrauch.

Die Anwendung wurde mit **Python (Flask)** entwickelt und speichert alle Daten bewusst in **CSV-Dateien**, um eine leichtgewichtige, datenbankfreie Architektur zu demonstrieren.

> Ziel des Projekts: Entwicklung einer strukturierten, modular aufgebauten Webanwendung mit Backend-Logik, Datenpersistenz, dynamischem Frontend und interaktiver Datenvisualisierung.

---

## 🚀 Features

### 👤 Profilverwaltung
- Erstellung und Löschung von Fitnessprofilen
- Speicherung von:
  - Name
  - Alter
  - Geschlecht
  - Körpergröße
  - Startgewicht
  - Zielgewicht
  - Trainingstage
  - Trainingsfokus
- Dynamische Aktualisierung des Trainingsfokus

---

### 📊 Fortschritts-Tracking
- Eingabe des aktuellen Gewichts
- Automatische BMI-Berechnung
- BMI-Kategorisierung:
  - Untergewicht
  - Normalgewicht
  - Übergewicht
  - Adipositas
- Speicherung aller Einträge mit Datum
- Historische Verlaufsdaten

---

### 🔥 Kalorienberechnung (MET-basiert)

Kalorien werden automatisch berechnet:

- Für Joggen & Radfahren  
  → basierend auf Trainingszeit (Minuten)

- Für alle anderen Trainingsarten  
  → basierend auf Fokus-Trainingsdauer

Formel:

Kalorien = MET × Körpergewicht × (Trainingszeit in Stunden)


MET-Werte sind im Code strukturiert hinterlegt und leicht erweiterbar.

---

### 🏃 Trainingsfokus & Übungen

Unterstützte Trainingsbereiche:

- Ganzkörper
- Arme
- Oberkörper
- Bauch/Rücken
- Beine/Po
- Joggen
- Radfahren
- Trampolin
- Yoga

Features:
- Dynamische Übungsauswahl (bis zu 6 zufällige Übungen)
- Textbeschreibung jeder Übung
- Optional: Bildanzeige pro Übung
- Interaktive "Weiter"-Navigation durch Übungen

---

### 📈 Interaktive Diagramme

Visualisierung mit **Chart.js**:

- Gewicht
- BMI
- Kalorienverbrauch
- Farbliche Markierung nach Trainingsfokus
- Zoom & Pan (chartjs-plugin-zoom)
- Tooltip-Zusatzinformationen
- Automatische Datumsachsen

---

## 🎨 UI / Design

- Modernes dunkles Theme
- Hightech-animierter Hintergrund (Canvas)
- Lokale Schriftarten (Roboto Mono)
- Responsive Layout
- Hover-Animationen
- Glas-Effekt (backdrop-filter)

Keine externen CSS-Frameworks – bewusst eigenständig umgesetzt.

---

## 🏗️ Architektur

### Backend
- Python 3
- Flask
- CSV-basierte Persistenz
- Trennung von:
  - Datenlogik
  - Berechnungslogik
  - Routen
  - Template-Rendering

### Frontend
- Jinja2 Templating
- Chart.js
- Vanilla JavaScript
- HTML5 + CSS3

---

## 📂 Projektstruktur

Fitnessapp/
│
├── app.py
├── profiles.csv
├── weight_history.csv
│
├── templates/
│ ├── select_profile.html
│ ├── new_profile.html
│ ├── index.html
│
├── static/
│ ├── css/
│ │ └── style.css
│ ├── fonts/
│ └── Bilder/
│
└── README.md


---

## 🧩 Installation & Setup

### Voraussetzungen

- Python 3.9+
- pip

---

### 1. Repository klonen

git clone https://github.com/Robotvalley19/Fitnessapp.git

cd Fitnessapp


---

### 2. Virtuelle Umgebung erstellen (empfohlen)

python3 -m venv venv
source venv/bin/activate # Linux / macOS
venv\Scripts\activate # Windows


---

### 3. Abhängigkeiten installieren

pip install flask


(Optional: `requirements.txt` für Produktionsumgebungen erstellen)

---

### 4. Anwendung starten


Im Browser öffnen:

http://localhost:5011


---

## 🍓 Raspberry Pi 4 Deployment

Die Anwendung läuft problemlos auf einem Raspberry Pi 4.

Optional:
- Autostart via systemd
- Reverse Proxy mit Nginx
- Betrieb im lokalen Netzwerk

---

## 🔒 Sicherheit & Designentscheidungen

- Keine externe Datenbank → bewusst minimalistische Architektur
- Keine Cloud-Abhängigkeit → vollständig offline nutzbar
- Lokale Fonts → keine CDN-Abhängigkeiten
- Keine personenbezogene Datenübertragung

---

## 📌 Mögliche Erweiterungen (Roadmap)

- Migration auf SQLite oder PostgreSQL
- Benutzer-Login-System
- REST-API
- Docker-Containerisierung
- Unit Tests (pytest)
- CI/CD Pipeline (GitHub Actions)
- Progressive Web App (PWA)
- Export als PDF-Bericht
- Deployment auf AWS / Azure

---

## 🎯 Projektziel

Dieses Projekt dient als:

- Demonstration von Full-Stack-Grundlagen
- Praxisbeispiel für Backend-Logik in Python
- Beispiel für interaktive Datenvisualisierung
- Portfolio-Projekt für Bewerbungen in:
  - Softwareentwicklung
  - Industrie-IT
  - Automatisierungstechnik
  - Embedded-/Edge-Systeme
  - Technische Informatik

---

## 👨‍💻 Autor

Robotvalley19  

Eigenständig entwickelt als praxisorientiertes Full-Stack-Projekt.
