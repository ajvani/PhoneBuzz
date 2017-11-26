# PhoneBuzz
https://infinite-oasis-27020.herokuapp.com/

### About
PhoneBuzz is a twist of the well-known FizzBuzz. 

Users can either send a call to play FizzBuzz, or they can receive
a call. 

Previous received calls are stored in a database. 

### Built With
- Backend: Flask (Python), Twilio API
- Frontend: HTML/CSS/JS/JQuery

### Setup
- Install Requirements:
```
pip install -r requirements.txt
```

- Setup Environment Variables:
```
export ACC_SID="<Your_Twilio_SID>"
export AUTH_TOK="<Your_Twilio_AUTH_TOK>"
export BASE_URL="<URL_for_hosting>"
```

- Setup HTML GET request WebHook for incoming calls in Twilio Console:
![Web Hook Example](./static/images/WebHookExample.png)

- Setup Flask App: 
```
export FLASK_APP=app.py
```

- Start Server:
```
flask run
```
