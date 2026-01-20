# Fitness-App

Eine **lokale Fitness-App** zur Verwaltung von Fitnessprofilen, Gewicht, BMI, Trainingsfokus und Übungen.  
Die App ist vollständig lokal und **browserbasiert**, speichert Daten in CSV-Dateien und benötigt keine externe Datenbank.

---

## 🚀 Features

- **Profile erstellen und bearbeiten**: Name, Alter, Geschlecht, Größe, Start- und Zielgewicht  
- **Trainingsplanung**: Auswahl von Trainingstagen und Trainingsfokus  
  *(Ganzkörper, Arme, Oberkörper, Bauch/Rücken, Beine/Po, Joggen, Trampolin, Radfahren, Yoga)*  
- **Gewichts- und BMI-Tracking**: Einfache Eingabe von Gewicht und Trainingszeit, automatische Berechnung von BMI und optionalen Kalorieninformationen  
- **Dynamische Anzeige von Übungen**: Übersichtliche Darstellung der Übungen, abhängig vom Trainingsfokus  
- **Interaktive Diagramme**: Verlauf von Gewicht und BMI visualisiert mit Chart.js  
- **Animierter Hightech-Hintergrund**: Modernes, animiertes Linienmuster auf jeder Seite für ein futuristisches UI-Erlebnis  
- **Lokale Datenspeicherung**: Alle Daten werden lokal in CSV-Dateien gespeichert (`profiles.csv` und `weight_history.csv`)  
- **Übungsbeschreibungen als Text & Bild**: Durch das Erstellen eines Verzeichnisses `static/Bilder` und das Einfügen von Bildern pro Übung ist eine visuelle Darstellung möglich  

---

## 🎨 Design & Fonts

Die App nutzt **lokale Fonts**, um Abmahnungen oder rechtliche Probleme zu vermeiden:

### Roboto Mono Regular & Bold
- Schriftart für Überschriften, Buttons, Labels und Eingabefelder  
- Die Fonts liegen lokal unter:
  - `static/fonts/RobotoMono-Regular.ttf`
  - `static/fonts/RobotoMono-Bold.ttf`  
- Vorteil: Die App funktioniert **offline**, ohne Internetverbindung zu Google Fonts

### CSS & Styling
- Moderne Farbpalette: dunkler Hintergrund (#0d0d0d) mit Akzentfarben (#00d1b2)  
- Transparente Container mit `backdrop-filter: blur()` für einen Glas-Effekt  
- Responsive Layout für alle Bildschirmgrößen  
- Eingabefelder und Buttons mit Hover-Effekten für bessere Interaktivität  

---

## 🧩 Installation & Setup auf Raspberry Pi 4

### 1. Repository klonen

```bash
git clone https://github.com/Robotvalley19/Fitnessapp.git
cd Fitnessapp
