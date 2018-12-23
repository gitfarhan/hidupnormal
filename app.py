from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, date
import string
import uuid
import random
import os
from flask_restful import Resource, Api
from urllib.parse import urlsplit

app = Flask(__name__)
api = Api(app)


def another_generator(length=8):
    return str(uuid.uuid1()).join(random.choices(string.ascii_uppercase + string.digits, k=5)).replace("-","")[:length]

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

        password = another_generator(length=10)
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

        # memisahkan hasil

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

# hidup normal API

class Encode(Resource):
    def get(self, code):
        url_data = urlsplit(code)
        dec = encrypt(url_data)

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
        delta = d0 - d1
        total = delta.days

        if total <= 0:
            return {'password' : password}
        else:
            return {'total' : total}

class GetPassword(Resource):
    def get(self, year, month, day):
        password = another_generator(length=10)
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

        result = {
            'date': fin,
            'total': total,
            'password': password,
            'code': code,
            'enc': enc
        }

        if total < 0:
            return {'error' : 'haha?'}
        else:
            return result

api.add_resource(GetPassword, '/get/<int:year>/<int:month>/<int:day>')
api.add_resource(Encode, '/encode/<string:code>')

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')

# if __name__ == "__main__":
#     app.run(debug=True, port=3000)
#     # password = another_generator(10)
#     # print(password)
#     # print(len(password))