from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, date
import string
import random
import os

app = Flask(__name__)

def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def anothe_generator(length=8):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

@app.route('/')
def index():
    return render_template('index.html')


def encrypt(message):
    result = ''
    for i in range(0, len(message)):
        result = result + chr(ord(message[i]) - 12)
    return result

def decrypt(message):
    result = ''
    for i in range(0, len(message)):
        result = result + chr(ord(message[i]) + 12)
    return result

@app.route('/insert', methods=['POST'])
def insert():
    tanggal = request.form['date']
    if tanggal:
        year = tanggal[:4]
        month = tanggal[5:7]
        day = tanggal[8:10]

        password = anothe_generator(length=10)
        gm = generator(size=8)
        email = '{m}@hidupnormal.net'.format(m=gm)
        code = '{d}{m}{y}{p}'.format(d=day, m=month, y=year, p=password)

        now = datetime.now()
        nowYear = now.year
        nowMonth = now.month
        nowDay = now.day

        d0 = date(int(year), int(month), int(day))
        d1 = date(nowYear, nowMonth, nowDay)
        delta = d0 - d1
        total = (delta.days)

        enc = encrypt(code)

        fin = "{day}/{month}/{year}".format(day=day, month=month, year=year)

        result = jsonify({
            'date' : fin,
            'total' : total,
            'password' : password,
            'email' : email,
            'code' : code,
            'enc' : enc
        })

        if total < 0:
            return jsonify({
                'error' : 'Haha?'
            })
        else:
            return result

    else:
        return jsonify({'error' : 'Missing data'})

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/process', methods=['POST'])
def process():
    kode = request.form['KodeInput']
    if kode:
        dec = decrypt(kode)

        # memsiahkan hasil

        day = dec[0:2]
        month = dec[2:4]
        year = dec[4:8]
        password = dec[8:]

        # menghitung sisa hari
        now = datetime.now()
        nowYear = now.year
        nowMonth = now.month
        nowDay = now.day

        d0 = date(int(year), int(month), int(day))
        d1 = date(nowYear, nowMonth, nowDay)
        delta = d0-d1
        total = delta.days

        datecode = "{day}/{month}/{year}".format(day=day, month=month, year=year)
        nowdate = "{day}/{month}/{year}".format(day=nowDay, month=nowMonth, year=nowYear)

        result_finished = jsonify({
            'password' : password
        })

        result_notfinished = jsonify({
            'total' : total
        })

        if total <= 0:
            return result_finished
        else:
            return result_notfinished
    else:
        return jsonify({
            "error" : "missing data"
        })


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')