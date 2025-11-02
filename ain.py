from flask import Flask, render_template, request, url_for, redirect
from datetime import date
import smtplib
from email.mime.text import MIMEText
import random
import time
import string
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__, template_folder="templates", static_folder="static")

# Streaky
streak_actual = 0
streak_before = 0
streak_high = 0

# Stav dne
message = False  # True pokud uživatel jedl těstoviny dnes
# Unikátní odkaz pro záchranu streak
random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

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

    #if password != "3.1415926535_pi":
        #return "Nesprávné heslo."

    if odpoved == "ano":
        streak_actual = streak_before
        streak_actual += 1
        streak_before += 1
        if streak_high < streak_actual:
            streak_high = streak_actual
        message = False
    else:
        streak_actual = 0
        message = True

    return redirect(url_for('prehled'))

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "krystof.ham@volny.cz"
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.volny.cz', 465) as server:
        server.login("krystof.ham@volny.cz", "Krystof26122009")
        server.sendmail("krystof.ham@volny.cz", to_email, msg.as_string())

def check_sent_mail():
    global message
    current_hour = int(time.strftime('%H', time.localtime()))
    if message :
        send_email("Streak Update", "Your streak is now 10.", "2612kiki@gmail.com")
        print("Email sent!")

# Spouštění každou hodinu pomocí APScheduleru
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_sent_mail, trigger="interval", hours=1)
scheduler.start()

if __name__ == '__main__':
    print(f"Unikátní odkaz pro záchranu streak: /{random_hash}")
    app.run(host='0.0.0.0', port=5000, debug=True)
