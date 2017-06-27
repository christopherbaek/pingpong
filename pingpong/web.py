import json
import logging
import requests

from flask import Flask, Response, redirect, render_template, request, url_for


# logging
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger('server')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)

# app
app = Flask(__name__)
firebase_token = None


@app.route('/')
def index():
    LOGGER.info('received index request')
    return render_template('index.html')


@app.route('/firebasetoken', methods=['POST'])
def save_firebase_token():
    LOGGER.info('received firebasetoken request')
    global firebase_token

    if 'firebaseToken' in request.form:
        firebase_token = request.form['firebaseToken']
        LOGGER.info('stored firebase token %s', firebase_token)
    else:
        LOGGER.info('firebaseToken not in form')

    return Response(status=204)


@app.route('/wake', methods=['POST'])
def wake():
    LOGGER.info('received wake request')
    send_firebase_message()
    return redirect(url_for('index'))


def send_firebase_message():
    if firebase_token is None:
        LOGGER.info('Unable to send firebase message without firebase token')
        return

    headers = {
        'Authorization': 'key={}'.format('AAAAPCzO2XY:APA91bG4aULWEJQrsPwdEGTvXJdLTX3wNYveT4Y5UEZAnjrYhiHVM6dI8F-m5CtxXDR3wPCEwsFNsZIGNuHrdPhDgMbygP33dx81JpFCQ5v3Q228seELPZOv3NmLVpNH3ZlWI940qa49'),
        'Content-Type': 'application/json'
    }

    message = {
        'to': firebase_token,
        'data': {
            'message': 'Wake up!'
        }
    }

    # example full message:
    #{
    #    "collapse_key": "score_update",
    #    "time_to_live": 108,
    #    "data": {
    #        "score": "4x8",
    #        "time": "15:16.2342"
    #    },
    #    "to" : "bk3RNwTe3H0:CI2k_HHwgIpoDKCIZvvDMExUdFQ3P1..."
    #}

    LOGGER.info('sending Firebase message: %s', json.dumps(message))
    response = requests.post(
        'https://fcm.googleapis.com/fcm/send',
        headers=headers,
        json=message)

    LOGGER.info('received response code: %d', response.status_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888')
