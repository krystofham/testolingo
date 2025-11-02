from flask import Flask, render_template, request, url_for, redirect
from datetime import date
import random
import string

app = Flask(__name__, template_folder="templates", static_folder="static")

streak_actual = 0
streak_before = 0
streak_high = 0

message = False  
random_hash = "safe_streak_dekuji_krystufku"
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
    return render_template('prehled.html',
                           streak_actual=streak_actual,
                           streak_before=streak_before,
                           streak_high=streak_high)

@app.route('/submit', methods=['POST'])
def submit():
    global streak_actual, streak_before, streak_high, message
    odpoved = request.form.get('odpoved')
    password = request.form.get('password')

    if password != "3.1415926535_pi":
        return "Nesprávné heslo."

    if odpoved == "ano":
        streak_actual = streak_before
        streak_actual += 1
        streak_before += 1
        if streak_high < streak_actual:
            streak_high = streak_actual
        message = False
    else:
        return redirect(url_for('sure'))

    return redirect(url_for('prehled'))
@app.route('/sure')
def sure():
    return render_template('sure.html')
@app.route('/urcite', methods=['POST'])
def urcite():
    global streak_actual, streak_before, streak_high, message
    odpoved = request.form.get('odpoved')
    if odpoved == "ano":
        streak_actual = streak_before
        streak_actual += 1
        streak_before += 1
        if streak_high < streak_actual:
            streak_high = streak_actual
        message = False
        return redirect(url_for('prehled'))
    elif odpoved == "ne":
        streak_actual = 0
        streak_before = 0
        message = True
        return redirect(url_for('nejim_testoviny'))
    return redirect(url_for('prehled'))

@app.route('/submit_streak', methods=['POST'])
def submit_streak():
    global streak_actual, streak_before, streak_high
    streak = request.form.get('streak')

    if streak is not None:
        streak_actual = int(streak)
        streak_before = streak_actual  # Assuming you want to set the previous streak to the current one
        if streak_high < streak_actual:
            streak_high = streak_actual

    return redirect(url_for('prehled'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)