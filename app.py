'''
author: Anmol Jadvani
app: PhoneBuzz
'''

import os
import time
import datetime
import sqlite3
import re
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from twilio.rest import Client
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# initial db setup on server start
conn = sqlite3.connect('./database.db')
schema = 'CREATE TABLE IF NOT EXISTS calls (time TEXT, number TEXT, delay TEXT, rurl TEXT)'
conn.execute(schema)
conn.close()

@app.route('/')
def homepage():
    # passing db to homepage values
    con = sqlite3.connect('./database.db')
    cur = con.cursor()
    calls = cur.execute('SELECT * FROM calls').fetchall()

    return render_template('index.html', calls=calls)


# fizzbuzz implementation
@app.route('/say_fizzbuzz', methods=['POST'])
def say_fizzbuzz():
    n = request.values.get('Digits', None)
    
    if n == None or not n.isdigit():
        n = 0
    else:
        n = int(n) 

    response = VoiceResponse()

    msg = " , ".join(["FizzBuzz" if x % 3 == 0 and x % 5 == 0 else\
            "Fizz" if x % 3 == 0 else "Buzz" if x % 5 == 0 else str(x)\
            for x in range(1, n)]) + " , End Fizzbuzz"

    response.say(msg)

    return str(response)

# handling incoming call 
@app.route('/handle_incoming', methods=['GET', 'POST'])
def handle_incoming():
    response = VoiceResponse()

    gather = Gather(action='/say_fizzbuzz', method='POST')

    gather.say('Enter the upper bound for fizzbuzz, followed by the pound symbol')

    response.append(gather)
    response.say('Thank you for using PhoneBuzz')

    return str(response)

# handling outgoing call
@app.route('/handle_outgoing', methods=['POST'])
def handle_outgoing(): 
    ACC_SID = os.environ['ACC_SID']
    AUTH_TOK = os.environ['AUTH_TOK']
    BASE_URL = os.environ['BASE_URL']

    delay = int(request.values.get('delay', 0))
    number = request.values.get('phone_number', None)

    rgx = '^[0-9]{10}|\([0-9]{3}\) ?[0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4}$'
    
    if number == None or re.search(rgx, number) == None:
        return redirect('/')

    # putting time delay
    time.sleep(delay)

    client = Client(ACC_SID, AUTH_TOK)

    rscm = BASE_URL + '/handle_db_update?delay=' + str(delay) + '&number=' + number
    url = BASE_URL + '/handle_incoming'

    call = client.calls.create(
        to=number,
        from_='+12013406597', 
        url=url,
        record=True,
        recording_status_callback=rscm
    )

    return redirect('/')

# updates db when needed
@app.route('/handle_db_update', methods=['POST'])
def handle_db_update(): 
    rec_url = request.values.get('RecordingUrl', None)
    number = request.values.get('number', None)
    delay = request.values.get('delay', None)

    time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    con = sqlite3.connect('database.db')

    try:
        cur = con.cursor()
        cur.execute('INSERT INTO calls (time, number, delay, rurl) VALUES (?,?,?,?)',\
                (time, number, delay, rec_url))
        con.commit()
    except:
        sqlite3.connect('database.db').rollback()
        print('Error: Could not insert into DB')

    return redirect('/') 

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
