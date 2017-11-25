'''
author: Anmol Jadvani
app: PhoneBuzz
'''

import os
import env
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/say_fizzbuzz')
def say_fizzbuzz():
    print('running')
    n = request.values.get('Digits', None)

    response = VoiceResponse()

    msg = "...".join(["FizzBuzz" if x % 3 == 0 and x % 5 == 0 else\
            "Fizz" if x % 3 == 0 else "Buzz" if x % 5 == 0 else str(x)\
            for x in range(1, n)]) + "... End Fizzbuzz"

    response.say(msg, voice="woman")

    print(str(response))
    return str(response)

@app.route('/handle_incoming')
def handle_incoming(methods=['GET']):
    response = VoiceResponse()

    gather = Gather(action='/say_fizzbuzz', method='POST')

    gather.say('Enter the upper bound for fizzbuzz, followed by the pound symbol')

    response.append(gather)
    response.say('Thank you for using PhoneBuzz')


    print(str(request.values))
    print(str(request.values.keys()))
    print(str(request.values.values()))
    print(str(request.values.get('Digits', None)))
    
    return str(response)

    

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
