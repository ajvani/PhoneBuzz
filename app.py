'''
author: Anmol Jadvani
app: PhoneBuzz
'''

import os
import time
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from twilio.rest import Client
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/say_fizzbuzz', methods=['GET', 'POST'])
def say_fizzbuzz():
    n = int(request.values.get('Digits', None))

    response = VoiceResponse()

    msg = "........".join(["FizzBuzz" if x % 3 == 0 and x % 5 == 0 else\
            "Fizz" if x % 3 == 0 else "Buzz" if x % 5 == 0 else str(x)\
            for x in range(1, n)]) + "................. End Fizzbuzz"

    response.say(msg)

    return str(response)

@app.route('/handle_incoming', methods=['GET','POST'])
def handle_incoming():
    response = VoiceResponse()

    gather = Gather(action='/say_fizzbuzz', method='POST')

    gather.say('Enter the upper bound for fizzbuzz, followed by the pound symbol')

    response.append(gather)
    response.say('Thank you for using PhoneBuzz')

    return str(response)

@app.route('/handle_outgoing', methods=['GET', 'POST'])
def handle_outgoing(): 

    delay = int(request.values.get('delay', 0))
    number = request.values.get('phone_number', None)

    # putting time delay
    time.sleep(delay)

    client = Client(ACC_SID, AUTH_TOK)
    rscm = 'https://infinite-oasis-27020.herokuapp.com/handle_db_update'

    call = client.calls.create(
        to=number,
        from_='+12013406597', 
        url='https://infinite-oasis-27020.herokuapp.com/handle_incoming',
        record=True,
        recording_status_callback=rscm
    )

    return redirect('/')

@app.route('/handle_db_update', methods=['GET', 'POST'])
def handle_db_update(): 
    print(request.values)

    return "none"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
