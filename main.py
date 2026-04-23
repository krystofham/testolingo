from flask import Flask, render_template, request, url_for, redirect, abort
import json
import os
import fcntl  
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY") 

PASSWORD = os.getenv("STREAK_PASSWORD")
DATA_FILE = Path("streak_data.json")


def check_password(password: str) -> bool:
    if not PASSWORD:
        abort(500)
    return password == PASSWORD


def load_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
            return data
    return {"streak_actual": 0, "streak_before": 0, "streak_high": 0, "message": False}


def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(data, f)
        fcntl.flock(f, fcntl.LOCK_UN)


def update_high(data: dict):
    if data["streak_actual"] > data["streak_high"]:
        data["streak_high"] = data["streak_actual"]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/prehled')
def prehled():
    data = load_data()
    return render_template('prehled.html',
                           streak_actual=data["streak_actual"],
                           streak_before=data["streak_before"],
                           streak_high=data["streak_high"])

@app.route('/nejim_testoviny')
def nejim_testoviny():
    return render_template('nejim_testoviny.html')

@app.route('/sure')
def sure():
    return render_template('sure.html')

@app.route('/submit', methods=['POST'])
def submit():
    if not check_password(request.form.get('password', '')):
        return "Nesprávné heslo.", 403  # správný HTTP status
    data = load_data()
    odpoved = request.form.get('odpoved')

    if odpoved == "ano":
        data["streak_actual"] = data["streak_before"] + 1
        data["streak_before"] = data["streak_actual"]
        update_high(data)
        data["message"] = False
        save_data(data)
        return redirect(url_for('prehled'))
    else:
        return redirect(url_for('sure'))


@app.route('/urcite', methods=['POST'])
def urcite():
    if not check_password(request.form.get('password', '')):
        return "Nesprávné heslo.", 403
    data = load_data()
    odpoved = request.form.get('odpoved')

    if odpoved == "ano":
        data["streak_actual"] = data["streak_before"] + 1
        data["streak_before"] = data["streak_actual"]
        update_high(data)
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
    if not check_password(request.form.get('password', '')):
        return "Nesprávné heslo.", 403

    data = load_data()
    streak_raw = request.form.get('streak')

    if streak_raw is not None:
        try:
            streak = int(streak_raw)
            if streak < 0: 
                return "Neplatná hodnota.", 400
        except ValueError:
            return "Neplatná hodnota.", 400

        data["streak_actual"] = streak
        data["streak_before"] = streak
        update_high(data)
        save_data(data)

    return redirect(url_for('prehled'))


if __name__ == '__main__':
    app.run()