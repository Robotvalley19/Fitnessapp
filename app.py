from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
import random

app = Flask(__name__)

PROFILE_FILE = "profiles.csv"
WEIGHT_FILE = "weight_history.csv"

# ---------------- Übungen ----------------
EXERCISES = {
    "Ganzkörper": [
        {"name": "Burpees", "description": "Beginne im aufrechten Stand, geh dann in die Hocke und setze die Hände auf den Boden. Springe mit den Füßen nach hinten in die Liegestützposition, führe optional einen Liegestütz aus und springe anschließend wieder mit den Füßen nach vorne. Richte dich aus der Hocke explosiv nach oben auf und strecke die Arme nach oben aus. Achte auf eine flüssige Bewegung und eine saubere Landung."},
        {"name": "Mountain Climbers", "description": "Nimm eine stabile Plank-Position ein und ziehe abwechselnd ein Knie zur Brust, während du den Körper stabil hältst. Die Hüfte bleibt möglichst ruhig und der Rücken gerade. Die Bewegung erfolgt schnell und kontrolliert, ohne dass das Becken nach oben oder unten kippt."},
        {"name": "Jumping Jacks", "description": "Springe aus dem Stand in eine breite Stellung, während du die Arme über den Kopf führst. Springe dann zurück in die Ausgangsposition, wobei die Arme wieder seitlich nach unten gehen. Halte den Rhythmus gleichmäßig und atme ruhig weiter."},
        {"name": "High Knees", "description": "Laufe auf der Stelle und ziehe dabei die Knie so hoch wie möglich, idealerweise bis auf Hüfthöhe. Halte den Oberkörper aufrecht und die Bauchmuskeln angespannt. Die Arme unterstützen die Bewegung, indem sie im Wechsel mit den Beinen schwingen."},
        {"name": "Squat to Press", "description": "Führe eine Kniebeuge aus, indem du das Gesäß nach hinten schiebst und die Knie beugst. Sobald du wieder nach oben kommst, drücke ein Gewicht oder eine Hantel kontrolliert über den Kopf. Senke die Arme wieder auf Schulterhöhe und wiederhole die Bewegung flüssig."},
        {"name": "Jump Squats", "description": "Beginne in der Kniebeuge, drücke dich explosiv nach oben und springe so hoch wie möglich. Landung weich mit gebeugten Knien, um die Gelenke zu schonen, und sofort wieder in die nächste Kniebeuge übergehen. Halte den Oberkörper aufrecht und die Bauchmuskeln aktiv."}
    ],

    "Arme": [
        {"name": "Bizepscurls", "description": "Stehe aufrecht und halte eine Hantel in jeder Hand. Beuge die Arme langsam nach oben, sodass die Hanteln Richtung Schultern gezogen werden. Die Ellenbogen bleiben dicht am Körper und bewegen sich nicht nach vorne. Senke die Hanteln kontrolliert wieder ab."},
        {"name": "Trizeps-Dips", "description": "Setze die Hände hinter dir auf eine Bank oder einen Stuhl und strecke die Beine nach vorne aus. Senke den Körper kontrolliert ab, indem du die Arme beugst, bis die Ellenbogen etwa 90 Grad erreichen. Drücke dich anschließend wieder hoch, bis die Arme gestreckt sind."},
        {"name": "Liegestütze", "description": "Lege dich in die Plank-Position und setze die Hände schulterbreit auf. Senke den Körper kontrolliert ab, bis die Brust fast den Boden berührt. Drücke dich dann kraftvoll nach oben, ohne den Rücken durchhängen zu lassen. Halte den Körper während der gesamten Bewegung gerade."},
        {"name": "Hammer Curls", "description": "Halte die Hanteln seitlich am Körper, die Handflächen zeigen zueinander. Beuge die Arme nach oben, ohne die Handgelenke zu drehen. Senke die Hanteln kontrolliert wieder ab. Diese Variante beansprucht den Unterarm und den äußeren Teil des Bizeps stärker."},
        {"name": "Front Raises", "description": "Halte eine Hantel in jeder Hand vor den Oberschenkeln. Hebe die Arme gerade nach vorne bis auf Schulterhöhe an und halte kurz. Senke die Arme langsam wieder ab. Achte darauf, dass der Oberkörper stabil bleibt und nicht mitschwingt."}
    ],

    "Oberkörper": [
        {"name": "Schulterdrücken", "description": "Halte eine Hantel in jeder Hand auf Schulterhöhe. Drücke die Hanteln kontrolliert über den Kopf, bis die Arme gestreckt sind. Senke die Hanteln langsam wieder auf Schulterhöhe ab. Achte darauf, den Rücken stabil zu halten und nicht ins Hohlkreuz zu fallen."},
        {"name": "Rudern", "description": "Beuge den Oberkörper leicht nach vorne, halte den Rücken gerade und ziehe die Hanteln oder ein Band Richtung Bauch. Die Ellenbogen werden nah am Körper geführt. Spanne die Schulterblätter zusammen und lasse die Arme kontrolliert wieder nach unten."},
        {"name": "Liegestütze breit", "description": "Führe Liegestütze mit einem breiteren Griff als üblich aus. Dadurch wird die Brust stärker beansprucht. Senke den Körper kontrolliert ab und drücke dich wieder hoch. Halte den Körper stabil und vermeide ein Durchhängen im Rücken."},
        {"name": "Reverse Fly", "description": "Beuge den Oberkörper leicht nach vorne und halte die Hanteln in beiden Händen. Hebe die Arme seitlich nach außen, bis sie auf Schulterhöhe sind, und spanne die Schulterblätter zusammen. Senke die Arme langsam wieder ab, ohne Schwung zu nutzen."},
        {"name": "Pull-Ups", "description": "Greife eine Klimmzugstange schulterbreit und hänge mit gestreckten Armen. Ziehe den Körper kontrolliert nach oben, bis das Kinn über der Stange ist. Senke dich langsam wieder ab. Halte den Körper gerade und vermeide Schwung aus den Beinen."}
    ],

    "Bauch/Rücken": [
        {"name": "Crunches", "description": "Lege dich auf den Rücken, stelle die Füße auf und lege die Hände hinter den Kopf. Hebe den Oberkörper leicht an, indem du die Bauchmuskeln anspannst, und senke ihn kontrolliert wieder ab. Achte darauf, dass der Nacken entspannt bleibt und die Bewegung aus dem Bauch kommt."},
        {"name": "Plank", "description": "Stütze dich auf Unterarmen und Zehen ab, der Körper bildet eine gerade Linie von Kopf bis Fuß. Spanne Bauch und Gesäß an und halte die Position so lange wie möglich. Vermeide ein Durchhängen im Rücken oder ein Hochziehen der Hüfte."},
        {"name": "Superman", "description": "Lege dich auf den Bauch und strecke Arme und Beine aus. Hebe gleichzeitig Arme und Beine leicht vom Boden ab und halte die Spannung für ein paar Sekunden. Senke dann langsam wieder ab. Diese Übung stärkt Rücken und Gesäß."},
        {"name": "Russian Twists", "description": "Setze dich auf den Boden, lehne den Oberkörper leicht zurück und hebe die Füße an, wenn möglich. Drehe den Oberkörper abwechselnd nach links und rechts, während du die Hände oder ein Gewicht vor dir hältst. Achte darauf, die Bewegung kontrolliert auszuführen und die Bauchmuskeln anzuspannen."},
        {"name": "Leg Raises", "description": "Lege dich auf den Rücken und strecke die Beine aus. Hebe die Beine langsam nach oben, bis sie senkrecht stehen, und senke sie kontrolliert wieder ab, ohne dass der Rücken vom Boden abhebt. Diese Übung trainiert besonders den unteren Bauchbereich."},
        {"name": "Bicycle Crunches", "description": "Lege dich auf den Rücken und hebe die Beine an. Führe abwechselnd den rechten Ellenbogen zum linken Knie und den linken Ellenbogen zum rechten Knie, während du die Beine in einer Fahrradbewegung bewegst. Achte darauf, dass die Bewegung langsam und kontrolliert erfolgt."}
    ],

    "Beine/Po": [
        {"name": "Kniebeugen", "description": "Stelle die Füße schulterbreit auf, spanne den Bauch an und schiebe das Gesäß nach hinten. Beuge die Knie, bis die Oberschenkel parallel zum Boden sind oder so tief wie möglich. Drücke dich dann wieder nach oben, ohne die Knie nach innen kippen zu lassen."},
        {"name": "Ausfallschritte", "description": "Mache einen großen Schritt nach vorne und senke das hintere Knie kontrolliert Richtung Boden. Das vordere Knie bleibt über dem Fuß. Drücke dich anschließend zurück in die Ausgangsposition und wechsle das Bein. Halte den Oberkörper aufrecht und die Bauchmuskeln angespannt."},
        {"name": "Glute Bridges", "description": "Lege dich auf den Rücken, stelle die Füße auf und drücke das Becken nach oben, bis der Körper eine gerade Linie bildet. Spanne das Gesäß am höchsten Punkt kurz an und senke das Becken kontrolliert wieder ab. Achte darauf, dass die Hüfte nicht durchhängt."},
        {"name": "Side Lunges", "description": "Mache einen großen Schritt zur Seite und beuge das vordere Bein, während das andere Bein gestreckt bleibt. Drücke dich anschließend wieder zurück in die Mitte und wiederhole die Bewegung auf der anderen Seite. Halte den Oberkörper aufrecht und die Knie in einer stabilen Linie."},
        {"name": "Calf Raises", "description": "Stelle dich aufrecht hin und hebe die Fersen langsam vom Boden, bis du auf den Zehenspitzen stehst. Halte kurz die Spannung und senke die Fersen kontrolliert wieder ab. Diese Übung stärkt die Wadenmuskulatur."},
        {"name": "Bulgarian Split Squats", "description": "Stelle einen Fuß hinter dir auf eine Bank oder einen Stuhl und halte den anderen Fuß vor dir. Senke den Körper kontrolliert ab, bis das vordere Knie etwa 90 Grad erreicht. Drücke dich dann wieder nach oben. Achte darauf, dass der Oberkörper aufrecht bleibt und das vordere Knie nicht über die Zehen hinausgeht."}
    ],

    "Trampolin": [
        {"name": "Basic Bounce", "description": "Springe locker und gleichmäßig auf dem Trampolin, ohne die Knie vollständig durchzudrücken. Halte die Sprünge kontrolliert und die Landung weich, um die Gelenke zu schonen."},
        {"name": "Jumping Jacks Trampolin", "description": "Führe Jumping Jacks auf dem Trampolin aus, indem du gleichzeitig die Beine seitlich öffnest und die Arme über den Kopf führst. Halte den Rhythmus konstant und nutze die Federung des Trampolins für einen sanften Sprung."},
        {"name": "High Knees Trampolin", "description": "Laufe auf dem Trampolin auf der Stelle und ziehe die Knie abwechselnd hoch. Achte darauf, dass du stabil bleibst und den Oberkörper aufrecht hältst. Die Sprünge sollten eher kurz und schnell sein."},
        {"name": "Twist Jumps", "description": "Springe auf dem Trampolin und drehe den Oberkörper leicht nach links und rechts, während die Füße zusammen bleiben. Die Drehung sollte kontrolliert erfolgen, damit du das Gleichgewicht hältst."},
        {"name": "Tuck Jumps", "description": "Springe hoch und ziehe die Knie zur Brust, während du in der Luft bist. Strecke die Beine wieder aus und lande weich auf dem Trampolin. Achte auf eine stabile Körpermitte und eine kontrollierte Landung."},
        {"name": "Seat Bounce", "description": "Springe kurz und lasse dich dann in eine sitzende Position fallen, ohne den Rücken zu belasten. Nutze die Federung des Trampolins, um direkt wieder nach oben zu kommen. Halte die Bewegung kontrolliert und rhythmisch."}
    ],

    "Joggen": [
        {"name": "Aufwärmen", "description": "Beginne mit 5 bis 10 Minuten lockerem Gehen oder sehr leichtem Joggen, um den Kreislauf in Schwung zu bringen und die Muskulatur aufzuwärmen. Achte auf eine ruhige Atmung und eine lockere Körperhaltung."},
        {"name": "Locker joggen", "description": "Jogge in einem moderaten Tempo, bei dem du noch gut sprechen kannst. Halte den Oberkörper aufrecht und die Schritte leicht. Diese Phase dient der Ausdauer und der Grundlagenausdauer."},
        {"name": "Intervalllauf", "description": "Wechsle zwischen schnellen und langsamen Abschnitten. Laufe z.B. 1 Minute schnell und 2 Minuten locker. Wiederhole diesen Wechsel mehrere Male. Diese Methode steigert die Ausdauer und verbessert die Geschwindigkeit."},
        {"name": "Tempo-Lauf", "description": "Laufe in einem schnelleren, aber kontrollierten Tempo, das du für mehrere Minuten halten kannst. Ziel ist es, die Ausdauer im höheren Belastungsbereich zu verbessern, ohne komplett zu erschöpfen."},
        {"name": "Cool-Down", "description": "Beende das Training mit 5 bis 10 Minuten lockerem Gehen oder sehr leichtem Joggen. Anschließend dehne die Muskulatur kurz, um die Regeneration zu fördern und den Puls langsam zu senken."}
    ],

    "Radfahren": [
        {"name": "Locker fahren", "description": "Fahre zu Beginn in einem entspannten Tempo, um die Muskulatur aufzuwärmen und die Beine auf die Belastung vorzubereiten. Achte auf eine gleichmäßige Trittfrequenz und eine aufrechte Haltung."},
        {"name": "Trittfrequenz", "description": "Fahre mit einer hohen Trittfrequenz bei niedrigem Widerstand, um die Beinmuskulatur zu aktivieren und die Ausdauer zu verbessern. Halte den Oberkörper ruhig und die Pedalbewegung gleichmäßig."},
        {"name": "Intervallfahrt", "description": "Wechsle zwischen schnellen und langsamen Abschnitten. Fahre z.B. 1 Minute sehr schnell und 2 Minuten locker. Wiederhole diesen Wechsel mehrere Male, um deine Geschwindigkeit und Ausdauer zu steigern."},
        {"name": "Bergsimulation", "description": "Erhöhe den Widerstand oder wähle eine Steigung, um die Muskulatur intensiver zu beanspruchen. Fahre in einem kraftvollen, gleichmäßigen Tempo und achte auf eine stabile Körperhaltung. Diese Phase stärkt Beine und Rumpf."},
        {"name": "Cool-Down", "description": "Fahre zum Abschluss 5 bis 10 Minuten locker, um den Puls zu senken und die Muskulatur zu entspannen. Danach kannst du die Beine leicht dehnen, um die Regeneration zu unterstützen."}
    ],

    "Yoga": [
        {"name": "Sonnengruß", "description": "Führe eine fließende Sequenz aus, bei der du Atem und Bewegung synchronisierst. Der Sonnengruß wärmt den Körper auf, mobilisiert die Gelenke und stärkt gleichzeitig die Muskulatur."},
        {"name": "Herabschauender Hund", "description": "Stelle dich in den Vierfüßlerstand und schiebe das Becken nach oben, bis der Körper eine umgekehrte V-Form bildet. Strecke die Arme und Beine und drücke die Fersen Richtung Boden. Diese Haltung dehnt Rücken, Schultern und Beine."},
        {"name": "Krieger", "description": "Stelle ein Bein nach vorne, beuge das vordere Knie und strecke das hintere Bein. Hebe die Arme nach oben und halte den Oberkörper aufrecht. Diese Haltung stärkt Beine, Hüften und Rumpf und verbessert die Stabilität."},
        {"name": "Baum", "description": "Stelle dich auf ein Bein und lege den Fuß des anderen Beins an den inneren Oberschenkel oder die Wade. Hebe die Arme nach oben und halte die Balance. Diese Übung fördert Gleichgewicht, Konzentration und Stabilität."},
        {"name": "Kindhaltung", "description": "Setze dich auf die Fersen, lege den Oberkörper nach vorne und strecke die Arme nach vorne oder entlang des Körpers aus. Entspanne den Rücken und atme tief ein und aus. Diese Haltung hilft, Stress abzubauen und den Körper zu beruhigen."}
    ]
}

# ---------------- MET ----------------
MET_VALUES = {
    "Joggen": 8,
    "Radfahren": 6,
    "Yoga": 3,

    "Burpees": 10,
    "Mountain Climbers": 8,
    "Jumping Jacks": 7,
    "High Knees": 8,
    "Squat to Press": 6,
    "Jump Squats": 9,

    "Bizepscurls": 3,
    "Trizeps-Dips": 4,
    "Liegestütze": 8,
    "Hammer Curls": 3,
    "Front Raises": 3,

    "Schulterdrücken": 5,
    "Rudern": 6,
    "Liegestütze breit": 8,
    "Reverse Fly": 4,
    "Pull-Ups": 8,

    "Crunches": 3,
    "Plank": 2.5,
    "Superman": 3,
    "Russian Twists": 3,
    "Leg Raises": 3,
    "Bicycle Crunches": 3,

    "Kniebeugen": 5,
    "Ausfallschritte": 5,
    "Glute Bridges": 3,
    "Side Lunges": 5,
    "Calf Raises": 3,
    "Bulgarian Split Squats": 6,

    "Basic Bounce": 4,
    "Jumping Jacks Trampolin": 6,
    "High Knees Trampolin": 6,
    "Twist Jumps": 6,
    "Tuck Jumps": 8,
    "Seat Bounce": 4
}

# ---------------- CSV ----------------
def read_profiles():
    if not os.path.exists(PROFILE_FILE):
        return []
    with open(PROFILE_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_profile(data):
    exists = os.path.exists(PROFILE_FILE)
    with open(PROFILE_FILE, 'a', newline='', encoding='utf-8') as f:
        fields = ['name','age','gender','height','start_weight','weight','goal_weight','training_days','training_focus']
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow(data)

def get_profile(name):
    for p in read_profiles():
        if p['name'] == name:
            return p
    return None

def update_profile_focus(name, focus):
    profiles = read_profiles()
    for p in profiles:
        if p['name'] == name:
            p['training_focus'] = focus
    with open(PROFILE_FILE, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=profiles[0].keys())
        w.writeheader()
        w.writerows(profiles)

def delete_profile(name):
    profiles = read_profiles()
    profiles = [p for p in profiles if p['name'] != name]
    if profiles:
        with open(PROFILE_FILE, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=profiles[0].keys())
            w.writeheader()
            w.writerows(profiles)
    else:
        if os.path.exists(PROFILE_FILE):
            os.remove(PROFILE_FILE)

    if os.path.exists(WEIGHT_FILE):
        with open(WEIGHT_FILE, newline='', encoding='utf-8') as f:
            rows = [r for r in csv.DictReader(f) if r['name'] != name]

        if rows:
            with open(WEIGHT_FILE, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=rows[0].keys())
                w.writeheader()
                w.writerows(rows)
        else:
            os.remove(WEIGHT_FILE)

def read_weight_history(name):
    if not os.path.exists(WEIGHT_FILE):
        return []
    with open(WEIGHT_FILE, newline='', encoding='utf-8') as f:
        return sorted([
            {
                'date': r['date'],
                'weight': float(r['weight']),
                'focus': r['focus'],
                'distance': float(r['distance']),
                'time': float(r['time']),
                'calories': float(r['calories'])
            }
            for r in csv.DictReader(f) if r['name'] == name
        ], key=lambda x: x['date'])

# ---------------- Gewichtseintrag ----------------
def add_weight_entry(name, weight, date, focus='', distance=0, time=0, focus_time=30):
    calories = 0

    # Joggen oder Radfahren (mit Zeitangabe)
    if focus in ["Joggen", "Radfahren"] and time > 0:
        calories = round(MET_VALUES[focus] * weight * (time / 60))

    # Alle anderen Trainingsfoki (mit Fokuszeit)
    elif focus in EXERCISES:
        duration_minutes = focus_time
        calories = round(MET_VALUES.get(focus, 4) * weight * (duration_minutes / 60))

    exists = os.path.exists(WEIGHT_FILE)
    with open(WEIGHT_FILE, 'a', newline='', encoding='utf-8') as f:
        fields = ['name','date','weight','focus','distance','time','calories']
        w = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            w.writeheader()
        w.writerow({
            'name': name,
            'date': date,
            'weight': weight,
            'focus': focus,
            'distance': distance,
            'time': time,
            'calories': calories
        })

# ---------------- BMI ----------------
def calculate_bmi(w, h):
    return round(w / ((float(h)/100)**2), 2)

def bmi_category(b):
    if b < 18.5: return "Untergewicht"
    if b < 25: return "Normalgewicht"
    if b < 30: return "Übergewicht"
    return "Adipositas"

# ---------------- Routes ----------------
@app.route('/')
def index():
    p = read_profiles()
    return render_template('select_profile.html', profiles=p) if p else redirect(url_for('new_profile'))

@app.route('/select', methods=['POST'])
def select_profile():
    return redirect(url_for('profile', name=request.form['name']))

@app.route('/new', methods=['GET','POST'])
def new_profile():
    if request.method == 'POST':
        d = request.form
        profile = {
            'name': d['name'],
            'age': d['age'],
            'gender': d['gender'],
            'height': d['height'],
            'start_weight': d['start_weight'],
            'weight': d['start_weight'],
            'goal_weight': d['goal_weight'],
            'training_days': ', '.join(d.getlist('training_days')),
            'training_focus': d['training_focus']
        }
        write_profile(profile)
        add_weight_entry(profile['name'], float(profile['weight']),
                         datetime.now().strftime('%Y-%m-%d'),
                         profile['training_focus'])
        return redirect(url_for('profile', name=profile['name']))
    return render_template('new_profile.html')

@app.route('/profile/<name>', methods=['GET','POST'])
def profile(name):
    profile = get_profile(name)

    if request.method == 'POST':

        # ---------------- Profil löschen ----------------
        if 'delete' in request.form:
            delete_profile(name)
            return redirect(url_for('index'))

        # ---------------- Fokus aktualisieren ----------------
        if 'update_focus' in request.form:
            new_focus = request.form['training_focus']
            profile['training_focus'] = new_focus
            update_profile_focus(name, new_focus)

        # ---------------- Gewicht speichern ----------------
        if 'save_weight' in request.form:
            weight = float(request.form['weight'])
            date = request.form['date']
            focus = profile['training_focus']

            if focus in ["Joggen", "Radfahren"]:
                distance = float(request.form['distance'])
                time = float(request.form['time'])
                add_weight_entry(name, weight, date, focus, distance=distance, time=time)
            else:
                focus_time = float(request.form['focus_time'])
                add_weight_entry(name, weight, date, focus, focus_time=focus_time)

            profile['weight'] = weight

    history = read_weight_history(name)
    bmi_list = [calculate_bmi(h['weight'], profile['height']) for h in history]

    return render_template(
        'index.html',
        profile=profile,
        history=history,
        bmi_list=bmi_list,
        current_bmi=bmi_list[-1] if bmi_list else 0,
        current_category=bmi_category(bmi_list[-1]) if bmi_list else '',
        exercises=random.sample(EXERCISES[profile['training_focus']], min(6, len(EXERCISES[profile['training_focus']]))),
        EXERCISES=EXERCISES,
        datetime=datetime
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)
