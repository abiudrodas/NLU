#!/usr/bin/python3
from flask import Flask, jsonify
from flask import make_response
from flask import request
# from flask_restful import Resource, Api
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from time import sleep
from nlu_cases.RRHH import RRHH


# defining the api-endpoint
if 'LOCAL' in os.environ:
    NLU_ENDPOINT = "http://localhost:5005/model/parse"
    CORE_ENDPOINT = "http://localhost:5006/webhooks/rest/webhook"
else:
    NLU_ENDPOINT = "http://nlu-service:5005/model/parse"
    CORE_ENDPOINT = "http://core-service:5006/webhooks/rest/webhook"

if 'TWILIO_SID' in os.environ:
    sid = os.environ['TWILIO_SID']
if 'TWILIO_TOKEN' in os.environ:
    token = os.environ['TWILIO_TOKEN']

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def send_whatsapp(msg, phone_to, attachment=None):
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = sid
    auth_token = token
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        from_='whatsapp:+14155238886',
        body=msg,
        to=phone_to,
        media_url=attachment
    )


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    rh = RRHH(NLU_url=NLU_ENDPOINT, Core_url=CORE_ENDPOINT)
    number = request.values.get('From')
    body = request.values.get('Body')
    attachaments = None

    data = {"message": body}
    answ = rh.post(r=data, sender_id=number)

    A = []
    for anw in answ:
        # print(anw["text"])
        if "media" in anw["text"]:
            attachaments = anw["text"].split(" ")[1]
            anw["text"] = ""
        send_whatsapp(anw["text"], number, attachment=attachaments)
        sleep(0.8)
        A.append(anw["text"])
    # print(A)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("\n\n".join(A))

    return ""


@app.route("/localtest", methods=['GET', 'POST'])
def sms_test():
    rh = RRHH(NLU_url=NLU_ENDPOINT, Core_url=CORE_ENDPOINT)
    answ = rh.post(r=request.json, sender_id="whatsapp:+34634146030")

    A = []
    for anw in answ:
        # print(anw["text"])
        A.append(anw["text"])
    # print(A)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("\n\n".join(A))

    return str(resp)


@app.route("/mms", methods=['GET', 'POST'])
def reply_mms():
    rh = RRHH(NLU_url=NLU_ENDPOINT, Core_url=CORE_ENDPOINT)
    number = "whatsapp:+34634146030"
    attachaments = None

    send_whatsapp("Ya puedo enviar ficheros por aquí bitch!!!!", number, attachment=attachaments)
    # print(A)
    return "OK"


'''-------------Finish new implementation---------------'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5060, debug=True, use_reloader=True)
