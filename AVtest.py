#!/usr/bin/python3
import sys
import json
from flask import Flask, jsonify
from flask import make_response, send_from_directory
from flask import request
from flask import abort
import os
#from flask_restful import Resource, Api
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import re
from datetime import datetime, timedelta
import calendar
import os
from os import environ
from time import sleep

# import locale
# locale.setlocale(locale.LC_ALL, 'es_ES')

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
#api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class RRHH():

    def __init__(self):
        self.nlu_message = {"text":None}
        self.dialog_message = {"message":None}
        self.basic_intents = ["greet", "fine_ask", "fine_normal", "thanks", "bye", "set_vacations",
                              "get_vacations_available", "negation", "affirmative", "password_reset"]

    def get_entities(self, NLU_response):
        entities_result = []
        if "entities" in NLU_response:
            entities = NLU_response["entities"]
            for entity in entities:
                tem_vect = []
                if entity['extractor'] == "CRFEntityExtractor":
                    tem_vect.append(entity["entity"])
                    tem_vect.append(entity["value"])
                    entities_result.append(tem_vect)
                elif entity['extractor'] == "DucklingHTTPExtractor":
                    if entity["entity"] == "time":
                        if "grain" in entity["additional_info"]:
                            tem_vect.append(entity["additional_info"]["grain"])
                            tem_vect.append(entity["value"])
                            entities_result.append(tem_vect)
                        elif entity["additional_info"]["type"] == "interval":
                            date_range = "from: " + entity["value"]["from"] + " - " + "to: " + entity["value"]["to"]
                            tem_vect.append(entity["additional_info"]["type"])
                            tem_vect.append(date_range)
                            entities_result.append(tem_vect)
                    elif entity["entity"] == "number":
                        tem_vect.append(entity["entity"])
                        tem_vect.append(entity["value"])
                        entities_result.append(tem_vect)
        return entities_result

    def _find_dates(self,string):
        return re.findall("\d{4}[-]?\d{1,2}[-]?\d{1,2}[T]\d{1,2}:\d{1,2}:\d{1,2}[.]?\d{1,3}[-]\d{1,2}:\d{1,2}", string)

    def Convert(self, a):
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct

    def NLU_adaptation(self, NLU_response):

        if "intent" in NLU_response:

            now = datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")
            hour = now.strftime("%H:%M:%S")
            days = list(calendar.day_name)

            if NLU_response["intent"]["name"] in self.basic_intents:
                self.dialog_message["message"] = NLU_response["intent"]["name"]

            elif NLU_response["intent"]["name"] == "user_number":
                entities = self.get_entities(NLU_response)
                for entity in entities:
                    new_dic = self.Convert(entity)
                    if entity[0] == "id_code":
                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'",'"')
                        #print(self.dialog_message)

            elif NLU_response["intent"]["name"] == "get_nomina":
                entities = self.get_entities(NLU_response)
                #print("Entidades: ",entities)
                months = ""
                if len(entities) == 0:
                    new_dic = {}
                    new_dic["month"] = month + " " + year
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')
                else:
                    for entity in entities:
                        new_dic = self.Convert(entity)
                        if entity[0] == "interval":
                            dates = self._find_dates(new_dic["interval"])
                            #print("DATES: ",dates)
                            new_dic["interval"] = ""
                            for date in dates:
                                date = date.split("-")
                                if int(date[0]) > int(year):
                                    date[0] = year
                                if int(date[1]) > int(month):
                                    date[1] = month
                                new_dic["interval"] = new_dic["interval"] + date[1] + " " + date[0] + " "
                            new_dic["interval"] = new_dic["interval"].strip()

                        elif entity[0] == "month":
                            dates = self._find_dates(new_dic["month"])
                            new_dic["month"] = ""
                            for date in dates:
                                date = date.split("-")
                                if int(date[0]) > int(year):
                                    date[0] = year
                                if int(date[1]) > int(month):
                                    date[1] = month
                            months = months + date[1] + " " + date[0] + "/"
                            new_dic["month"] = months
                            new_dic["month"] = new_dic["month"].strip("/")

                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

            elif NLU_response["intent"]["name"] in ["set_schedule_in", "set_schedule_out"]:
                entities = self.get_entities(NLU_response)
                #print("Entidades: ",entities)

                if len(entities) > 0:
                    for entity in entities:
                        new_dic = self.Convert(entity)
                        #print(new_dic)
                        if entity[0] in ["day", "hour"]:
                            dates = self._find_dates(new_dic[entity[0]])
                            for date in dates:
                                date = date.split('T')
                                user_date = date[0]
                                user_hour_temp = date[1].split(".")
                                user_hour = user_hour_temp[0]

                                user_date = user_date.split("-")
                                date_format = "%d/%m/%Y"
                                user_date_formated = datetime.strptime(
                                    user_date[2] + "/" + user_date[1] + "/" + user_date[0], date_format)
                                now = datetime.strptime(day + "/" + month + "/" + year, date_format)

                                if user_date_formated > now:
                                    user_day_ = [word for word in days if word in NLU_response["text"]]
                                    if entity[0] == "hour":
                                        if len(user_day_) < 1:
                                            delta = user_date_formated - now
                                            real_date = user_date_formated - delta
                                            real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
                                            new_dic = {"day": user_hour + " " + real_date}
                                        else:
                                            real_date = user_date_formated - timedelta(days=7)
                                            real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime(
                                                '%d/%m/%Y')
                                            new_dic = {"day": user_hour + " " + real_date}

                                    elif entity[0] == "day":
                                        real_date = user_date_formated - timedelta(days=7)
                                        #print(real_date)
                                        real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime(
                                            '%d/%m/%Y')
                                        new_dic = {"day": user_hour + " " + real_date}


                                else:
                                    real_date = datetime.strptime(str(user_date_formated), '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d/%m/%Y')
                                    new_dic = {"day": user_hour + " " + str(real_date)}

                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(
                        new_dic).replace("'", '"')

                else:
                    register = hour + " " + day + "/" + month + "/" + year
                    new_dic = {"day":register}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

            elif NLU_response["intent"]["name"] in ["get_schedule_in", "get_schedule_out"]:
                entities = self.get_entities(NLU_response)
                if len(entities) == 0:

                    register = day + "/" + month + "/" + year
                    new_dic = {"day": register}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

                else:
                    for entity in entities:
                        new_dic = self.Convert(entity)
                        if entity[0] == "day":
                            dates = self._find_dates(new_dic[entity[0]])
                            for date in dates:
                                date = date.split('T')
                                user_date = date[0]

                                user_date = user_date.split("-")
                                date_format = "%d/%m/%Y"
                                user_date_formated = datetime.strptime(
                                    user_date[2] + "/" + user_date[1] + "/" + user_date[0], date_format)
                                real_date = datetime.strptime(str(user_date_formated), '%Y-%m-%d %H:%M:%S').strftime(
                                    '%d/%m/%Y')
                                new_dic = {"day": real_date}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(
                        new_dic).replace("'", '"')

            elif NLU_response["intent"]["name"] == "vacation_range":
                entities = self.get_entities(NLU_response)

                for entity in entities:
                    new_dic = self.Convert(entity)
                    if entity[0] == "interval":
                        dates = self._find_dates(new_dic["interval"])
                        #print("DATES: ", dates)
                        new_dic["interval"] = ""
                        for date in dates:
                            date = date.split('T')
                            user_date = date[0]
                            user_date = user_date.split("-")
                            date_format = "%d/%m/%Y"
                            user_date_formated = datetime.strptime(
                                user_date[2] + "/" + user_date[1] + "/" + user_date[0], date_format)
                            real_date = datetime.strptime(str(user_date_formated), '%Y-%m-%d %H:%M:%S').strftime(
                                '%d/%m/%Y')
                            new_dic["interval"] = new_dic["interval"] + real_date + " "
                        new_dic["interval"] = new_dic["interval"].strip()
                        #print(new_dic)
                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(
                            new_dic).replace("'", '"')

                    elif entity[0] == "day":
                        dates = self._find_dates(new_dic["day"])
                        new_dic["day"] = ""
                        if len(dates) == 1:
                            date = dates[0].split('T')
                            user_date_formated = datetime.strptime(date[0], '%Y-%m-%d')
                            real_date = datetime.strptime(str(user_date_formated), '%Y-%m-%d %H:%M:%S').strftime(
                                '%d/%m/%Y')
                            new_dic["day"] = real_date
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

        return self.dialog_message

    def post(self, r):

        if "message" in r:
            self.nlu_message["text"] = r["message"]
            #print("NLU_message",self.nlu_message)
            NLU_response = requests.post(url=NLU_ENDPOINT, json=self.nlu_message)
            dialog_message = self.NLU_adaptation(NLU_response.json())
            #print("Dialog Manager: ",dialog_message)
            dialog_answ = requests.post(url=CORE_ENDPOINT, json=dialog_message)

        return dialog_answ.json()
        #return "OK"


    def send_whatsapp(self, msg, phone_to,attachment=None):
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
            media_url = attachment
        )

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    rh = RRHH()
    urls_templates = ["http://", "https://"]
    number = request.values.get('From')
    body = request.values.get('Body')
    attachaments = None

    data = {"message":body}
    answ = rh.post(r=data)

    A = []
    for anw in answ:
        #print(anw["text"])
        if any(url in anw["text"] for url in urls_templates):
            attachaments = anw["text"]
            anw["text"] = ""
        rh.send_whatsapp(anw["text"],number, attachment=attachaments)
        sleep(0.5)
        A.append(anw["text"])
    #print(A)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("\n\n".join(A))

    return ""

@app.route("/localtest", methods=['GET', 'POST'])
def sms_test():
    rh = RRHH()
    answ = rh.post(r=request.json)

    A = []
    for anw in answ:
        #print(anw["text"])
        A.append(anw["text"])
    #print(A)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("\n\n".join(A))

    return str(resp)

@app.route("/mms", methods=['GET', 'POST'])
def reply_mms():
    rh = RRHH()
    number = "whatsapp:+34634146030"
    attachaments = None

    rh.send_whatsapp("Ya puedo enviar ficheros por aquí bitch!!!!", number, attachment=attachaments)
    #print(A)
    return "OK"


'''-------------Finish new implementation---------------'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5060, debug=True, use_reloader=True)