import sys
import json
from flask import Flask, jsonify
from flask import make_response, send_from_directory
from flask import request
from flask import abort
import os
from flask_restful import Resource, Api
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse


# defining the api-endpoint
NLU_ENDPOINT = "http://localhost:5005/model/parse"
CORE_ENDPOINT = "http://localhost:5006/webhooks/rest/webhook"

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class RRHH():

    def __init__(self):
        self.nlu_message = {"text":None}
        self.dialog_message = {"message":None}
        self.basic_intents = ["greet", "fine_ask", "fine_normal", "thanks", "bye", "set_vacations",
                              "get_vacations_available", "set_schedule_in", "set_schedule_out", "vacation_range",
                              "get_nomina"]

    def get_entities(self, NLU_response):
        entities_result = []
        if "entities" in NLU_response:
            entities = NLU_response["entities"]
            for entity in entities:
                tem_vect = []
                tem_vect.append(entity["entity"])
                tem_vect.append(entity["value"])
                entities_result.append(tem_vect)
        return entities_result

    def Convert(self, a):
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct

    def NLU_adaptation(self, NLU_response):
        if "intent" in NLU_response:
            if NLU_response["intent"]["name"] in self.basic_intents:
                self.dialog_message["message"] = NLU_response["intent"]["name"]

            elif NLU_response["intent"]["name"] == "user_number":
                entities = self.get_entities(NLU_response)
                for entity in entities:
                    new_dic = self.Convert(entity)
                    if entity[0] == "id_code":
                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'",'"')
                        print(self.dialog_message)
        return self.dialog_message

    def post(self, r):

        if "message" in r:
            self.nlu_message["text"] = r["message"]
            print("NLU_message",self.nlu_message)
            NLU_response = requests.post(url=NLU_ENDPOINT, json=self.nlu_message)
            dialog_message = self.NLU_adaptation(NLU_response.json())
            print(dialog_message)
            dialog_answ = requests.post(url=CORE_ENDPOINT, json=dialog_message)

        return dialog_answ.json()

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    rh = RRHH()
    number = request.values.get('From')
    body = request.values.get('Body')

    data = {"message":body}
    answ = rh.post(r=data)

    A = []
    for anw in answ:
        print(anw["text"])
        A.append(anw["text"])
    print(A)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("\n\n".join(A))

    return str(resp)

'''-------------Finish new implementation---------------'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5060, debug=True, use_reloader=True)