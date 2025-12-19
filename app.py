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
        {"name": "Burpees", "description": "Starte aus dem Stehen. Gehe in die Hocke. Hände auf Boden, springe in Liegestützposition, führe Liegestütz aus, zurück in Hocke, dann explosiv nach oben."},
        {"name": "Mountain Climbers", "description": "Plank-Position. Knie schnell Richtung Brust ziehen, Core angespannt."},
        {"name": "Jumping Jacks", "description": "Aufrecht springen, Beine spreizen, Arme hoch, zurück. Landung leicht gebeugt."},
        {"name": "High Knees", "description": "Auf der Stelle laufen, Knie hoch, Arme mitschwingen, Rücken gerade."},
        {"name": "Squat to Press", "description": "Kniebeuge, beim Aufstehen Hanteln/Wasserflaschen über Kopf drücken, Core angespannt."},
        {"name": "Jump Squats", "description": "Kniebeuge, explosiv springen, sanft landen, kontrolliert wiederholen."}
    ],
    "Arme": [
        {"name": "Bizepscurls", "description": "Hanteln parallel, langsam Arme beugen, kurz halten, langsam absenken, Ellbogen stabil."},
        {"name": "Trizeps-Dips", "description": "Auf Bank/Stuhl Hände abstützen, Ellenbogen beugen, Hüfte absenken und hochdrücken."},
        {"name": "Liegestütze", "description": "Körper gerade, Hände schulterbreit, Brust Richtung Boden, wieder hochdrücken."},
        {"name": "Hammer Curls", "description": "Hanteln parallel halten, Unterarme beugen, kurz halten, langsam absenken."},
        {"name": "Front Raises", "description": "Hanteln/Flaschen vor Oberschenkel halten, Arme gerade nach vorn heben bis Schulterhöhe, kontrolliert absenken."}
    ],
    "Oberkörper": [
        {"name": "Schulterdrücken", "description": "Hanteln auf Schulterhöhe, Arme über Kopf strecken, kontrolliert absenken."},
        {"name": "Rudern", "description": "Hanteln in Händen, Oberkörper leicht vorgebeugt, Hanteln Richtung Bauch ziehen, langsam absenken."},
        {"name": "Liegestütze breit", "description": "Hände weiter als Schulterbreit, Körper gerade, Brust absenken, wieder hochdrücken."},
        {"name": "Reverse Fly", "description": "Oberkörper leicht vorgebeugt, Arme hängen, Hanteln seitlich heben, langsam absenken."},
        {"name": "Pull-Ups", "description": "An Stange, Hände schulterbreit, hochziehen bis Kinn über Stange, kontrolliert absenken."}
    ],
    "Bauch/Rücken": [
        {"name": "Crunches", "description": "Rücken auf Matte, Beine angewinkelt, Hände hinter Kopf, Oberkörper heben, langsam absenken."},
        {"name": "Plank", "description": "Unterarme/Zehen auf Boden, Körper gerade, Bauchmuskeln angespannt, Position halten."},
        {"name": "Superman", "description": "Auf Bauch liegen, Arme und Beine gleichzeitig anheben, kurz halten, langsam absenken."},
        {"name": "Russian Twists", "description": "Rücken leicht nach hinten, Beine angewinkelt, Hände zusammen, Oberkörper rechts/links drehen."},
        {"name": "Leg Raises", "description": "Auf Rücken, Beine gestreckt, langsam bis 90° anheben, langsam absenken."},
        {"name": "Bicycle Crunches", "description": "Rücken auf Boden, Hände hinter Kopf, Ellenbogen zum gegenüberliegenden Knie bringen, Beine abwechselnd bewegen."}
    ],
    "Beine/Po": [
        {"name": "Kniebeugen", "description": "Füße schulterbreit, Rücken gerade, Bauch angespannt, Knie beugen, Po nach hinten, wieder hochdrücken."},
        {"name": "Ausfallschritte", "description": "Schritt nach vorn, hinteres Knie Richtung Boden, vorderes Knie nicht über Zehen, wieder hochdrücken, Bein wechseln."},
        {"name": "Glute Bridges", "description": "Auf Rücken, Füße auf Boden, Hüfte hochdrücken, Po anspannen, langsam absenken."},
        {"name": "Side Lunges", "description": "Seitlich Schritt, Knie beugen, Po nach hinten, zurück, andere Seite."},
        {"name": "Calf Raises", "description": "Auf Zehenspitzen hochdrücken, kurz halten, langsam absenken."},
        {"name": "Bulgarian Split Squats", "description": "Hinteres Bein auf Bank, vorderes stabil, Knie beugen, Po nach unten, wieder hochdrücken."}
    ],
    "Trampolin": [
        {"name": "Basic Bounce", "description": "Auf Trampolin, Knie leicht gebeugt, sanft springen, Rücken gerade, Arme locker mitschwingen."},
        {"name": "Jumping Jacks Trampolin", "description": "Auf Trampolin Jumping Jack Position springen, zurück, weich landen."},
        {"name": "High Knees Trampolin", "description": "Auf Trampolin laufen, Knie hoch, Core aktiv, Arme mitschwingen."},
        {"name": "Twist Jumps", "description": "Leicht hochspringen, Oberkörper rechts/links drehen, kontrolliert landen."},
        {"name": "Tuck Jumps", "description": "Hoch springen, Knie Richtung Brust ziehen, kurz halten, langsam abrollen."},
        {"name": "Seat Bounce", "description": "Kurz setzen, aufstehen, sanft landen, Core stabil."}
    ],
    "Joggen": []
}

# ---------------- MET-Werte für Kalorien ----------------
MET_VALUES = {
    "Joggen": 8,
    "Burpees": 10,
    "Mountain Climbers": 8,
    "Jumping Jacks": 8,
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

# ---------------- CSV Handling ----------------
def read_profiles():
    profiles = []
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['name'] = row['name'].strip()
                profiles.append(row)
    return profiles

def write_profile(profile_data):
    file_exists = os.path.exists(PROFILE_FILE)
    with open(PROFILE_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = [
            'name', 'age', 'gender', 'height', 'start_weight', 'weight',
            'goal_weight', 'training_days', 'training_focus'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        profile_data['name'] = profile_data['name'].strip()
        writer.writerow(profile_data)

def get_profile(name):
    name = name.strip()
    profiles = read_profiles()
    for p in profiles:
        if p['name'] == name:
            return p
    return None

def update_profile_focus(name, new_focus):
    profiles = read_profiles()
    for p in profiles:
        if p['name'] == name:
            p['training_focus'] = new_focus
    with open(PROFILE_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name','age','gender','height','start_weight','weight','goal_weight','training_days','training_focus']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)

def read_weight_history(name):
    name = name.strip()
    history = []
    if os.path.exists(WEIGHT_FILE):
        with open(WEIGHT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['name'].strip() == name:
                    history.append({
                        'date': row['date'], 
                        'weight': float(row['weight']),
                        'focus': row.get('focus',''),
                        'distance': float(row.get('distance',0)),
                        'time': float(row.get('time',0)),
                        'calories': float(row.get('calories',0))
                    })
    return sorted(history, key=lambda x: x['date'])

# ---------------- Kalorienberechnung mit MET ----------------
def add_weight_entry(name, weight, focus=None, distance=0, time=0):
    name = name.strip()
    calories = 0

    if focus == "Joggen" and distance > 0 and time > 0:
        met = MET_VALUES.get("Joggen", 8)
        hours = time / 60
        calories = round(met * weight * hours)
    elif focus in EXERCISES and focus != "Joggen":
        total_calories = 0
        for ex in EXERCISES[focus]:
            ex_name = ex['name']
            met = MET_VALUES.get(ex_name, 4)
            duration_hours = 5 / 60  # 5 Minuten pro Übung
            total_calories += met * weight * duration_hours
        calories = round(total_calories)

    file_exists = os.path.exists(WEIGHT_FILE)
    with open(WEIGHT_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'date', 'weight', 'focus', 'distance', 'time', 'calories']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'name': name,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'weight': weight,
            'focus': focus if focus else '',
            'distance': distance,
            'time': time,
            'calories': calories
        })

def delete_profile(name):
    name = name.strip()
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            profiles = [row for row in reader if row['name'].strip() != name]
        with open(PROFILE_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name','age','gender','height','start_weight','weight','goal_weight','training_days','training_focus']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(profiles)
    if os.path.exists(WEIGHT_FILE):
        with open(WEIGHT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            history = [row for row in reader if row['name'].strip() != name]
        with open(WEIGHT_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['name','date','weight','focus','distance','time','calories']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(history)

# ---------------- BMI ----------------
def calculate_bmi(weight, height):
    try:
        height_m = float(height) / 100
        bmi = float(weight) / (height_m ** 2)
        return round(bmi, 2)
    except:
        return 0

def bmi_category(bmi):
    if bmi == 0:
        return "Keine Daten"
    elif bmi < 18.5:
        return "Untergewicht"
    elif bmi < 25:
        return "Normalgewicht"
    elif bmi < 30:
        return "Übergewicht"
    else:
        return "Adipositas"

# ---------------- Übungen für Fokus ----------------
def get_exercises_for_focus(focus):
    if focus in EXERCISES:
        return random.sample(EXERCISES[focus], k=min(6, len(EXERCISES[focus])))
    return []

# ---------------- Routes ----------------
@app.route('/')
def index():
    profiles = read_profiles()
    if profiles:
        return render_template('select_profile.html', profiles=profiles)
    else:
        return redirect(url_for('new_profile'))

@app.route('/select', methods=['POST'])
def select_profile():
    name = request.form.get('name').strip()
    return redirect(url_for('profile', name=name))

@app.route('/new', methods=['GET','POST'])
def new_profile():
    if request.method == 'POST':
        data = {
            'name': request.form['name'].strip(),
            'age': request.form['age'],
            'gender': request.form['gender'],
            'height': request.form['height'],
            'start_weight': request.form['start_weight'],
            'weight': request.form['start_weight'],
            'goal_weight': request.form['goal_weight'],
            'training_days': ', '.join(request.form.getlist('training_days')),
            'training_focus': request.form['training_focus']
        }
        write_profile(data)
        add_weight_entry(data['name'], float(data['start_weight']), data['training_focus'])
        return redirect(url_for('profile', name=data['name']))
    return render_template('new_profile.html')

@app.route('/profile/<name>', methods=['GET','POST'])
def profile(name):
    name = name.strip()
    profile = get_profile(name)
    if not profile:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'delete' in request.form:
            delete_profile(name)
            return redirect(url_for('index'))
        elif 'update_focus' in request.form:
            profile['training_focus'] = request.form['training_focus']
            update_profile_focus(name, profile['training_focus'])
        else:
            new_weight = float(request.form.get('weight', profile['weight']))
            distance = float(request.form.get('distance', 0))
            time = float(request.form.get('time', 0))
            focus_today = profile.get('training_focus', '')
            add_weight_entry(name, new_weight, focus=focus_today, distance=distance, time=time)
            profile['weight'] = new_weight

    history = read_weight_history(name)
    bmi_list = [calculate_bmi(entry['weight'], profile['height']) for entry in history]
    current_bmi = bmi_list[-1] if bmi_list else 0
    current_category = bmi_category(current_bmi)
    exercises = get_exercises_for_focus(profile['training_focus'])

    return render_template('index.html', profile=profile, history=history, bmi_list=bmi_list,
                           current_bmi=current_bmi, current_category=current_category,
                           exercises=exercises, EXERCISES=EXERCISES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)
