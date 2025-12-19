# Fitnessapp

Eine **lokale Fitness-App** zur Verwaltung von Fitnessprofilen, Gewicht, BMI, Trainingsfokus und Übungen.  
Die App ist vollständig lokal und **browserbasiert**, speichert Daten in CSV-Dateien und benötigt keine externe Datenbank.

---

## Features

- **Profile erstellen und bearbeiten**: Name, Alter, Geschlecht, Größe, Start- und Zielgewicht.  
- **Trainingsplanung**: Auswahl von Trainingstagen und Trainingsfokus (Ganzkörper, Arme, Oberkörper, Bauch/Rücken, Beine/Po, Joggen, Trampolin).  
- **Gewichts- und BMI-Tracking**: Einfache Eingabe von Gewicht, automatische Berechnung von BMI und optionalen Kalorieninformationen.  
- **Dynamische Anzeige von Übungen**: Übersichtliche Darstellung der Übungen, abhängig vom Trainingsfokus.  
- **Interaktive Diagramme**: Verlauf von Gewicht und BMI visualisiert mit Chart.js.  
- **Animierter Hightech-Hintergrund**: Modernes, animiertes Linienmuster auf jeder Seite für ein futuristisches UI-Erlebnis.  
- **Lokale Datenspeicherung**: Alle Daten werden lokal in CSV-Dateien gespeichert (`profiles.csv` und `weight_history.csv`).  

---

## Design & Fonts

Die App nutzt **lokale Fonts**, um Abmahnungen oder rechtliche Probleme zu vermeiden:  

- **Roboto Mono Regular & Bold**:  
  - Schriftart für Überschriften, Buttons, Labels und Eingabefelder.  
  - Die Fonts liegen lokal unter `static/fonts/RobotoMono-Regular.ttf` und `RobotoMono-Bold.ttf`.  
  - Vorteil: die App funktioniert **offline** ohne Internetverbindung zu Google Fonts.  

**CSS & Styling**:  
- Moderne Farbpalette: dunkler Hintergrund (#0d0d0d) mit Akzentfarben (#00d1b2) für Buttons, Überschriften und Rahmen.  
- Transparente Container mit `backdrop-filter: blur()` für Glas-Effekt.  
- Responsive Layout für alle Bildschirmgrößen.  
- Eingabefelder und Buttons mit Hover-Effekten für bessere Interaktivität.  

---

## Installation

1. Repository klonen:
```bash
git clone https://github.com/Robotvalley19/Fitnessapp.git
cd Fitnessapp
