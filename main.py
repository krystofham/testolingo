from flask import Flask, render_template, request, url_for, redirect
import json
from pathlib import Path

app = Flask(__name__, template_folder="templates", static_folder="static")

DATA_FILE = Path("streak_data.json")

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"streak_actual": 0, "streak_before": 0, "streak_high": 0, "message": False}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


@app.route('/safe_streak_dekuji_krystufku')
def safe():
    return render_template('safe.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nejim_testoviny')
def nejim_testoviny():
    return render_template('nejim_testoviny.html')

@app.route('/prehled')
def prehled():
    data = load_data()
    return render_template('prehled.html',
                           streak_actual=data["streak_actual"],
                           streak_before=data["streak_before"],
                           streak_high=data["streak_high"])

@app.route('/submit', methods=['POST'])
def submit():
    data = load_data()
    odpoved = request.form.get('odpoved')
    password = request.form.get('password')

    if password != "3.1415926535_pi":
        return "Nesprávné heslo."

    if odpoved == "ano":
        data["streak_actual"] = data["streak_before"] + 1
        data["streak_before"] = data["streak_actual"]
        if data["streak_high"] < data["streak_actual"]:
            data["streak_high"] = data["streak_actual"]
        data["message"] = False
        save_data(data)
        return redirect(url_for('prehled'))
    else:
        return redirect(url_for('sure'))

@app.route('/sure')
def sure():
    return render_template('sure.html')

@app.route('/urcite', methods=['POST'])
def urcite():
    data = load_data()
    odpoved = request.form.get('odpoved')

    if odpoved == "ano":
        data["streak_actual"] = data["streak_before"] + 1
        data["streak_before"] = data["streak_actual"]
        if data["streak_high"] < data["streak_actual"]:
            data["streak_high"] = data["streak_actual"]
        data["message"] = False
        save_data(data)
        return redirect(url_for('prehled'))
    elif odpoved == "ne":
        data["streak_actual"] = 0
        data["streak_before"] = 0
        data["message"] = True
        save_data(data)
        return redirect(url_for('nejim_testoviny'))
    return redirect(url_for('prehled'))

@app.route('/submit_streak', methods=['POST'])
def submit_streak():
    data = load_data()
    streak = request.form.get('streak')

    if streak is not None:
        data["streak_actual"] = int(streak)
        data["streak_before"] = data["streak_actual"]
        if data["streak_high"] < data["streak_actual"]:
            data["streak_high"] = data["streak_actual"]
        save_data(data)

    return redirect(url_for('prehled'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)