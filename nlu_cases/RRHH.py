import requests
from datetime import datetime, timedelta
import calendar
from nlu_cases.nlu_utils import NLU_utils


class RRHH():

    def __init__(self, NLU_url=None, Core_url=None):
        self.nlu_message = {"text": None}
        self.dialog_message = {"message": None}
        self.basic_intents = ["greet", "fine_ask", "fine_normal", "thanks", "bye", "set_vacations",
                              "get_vacations_available", "negation", "affirmative", "password_reset"]
        self.nlu_uts = NLU_utils()
        self.NLU_ENDPOINT = NLU_url
        self.CORE_ENDPOINT = Core_url
        self.user_id = None

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
                entities = self.nlu_uts.get_entities(NLU_response)
                for entity in entities:
                    new_dic = self.nlu_uts.Convert(entity)
                    if entity[0] == "id_code":
                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')
                        # print(self.dialog_message)

            elif NLU_response["intent"]["name"] == "category_appointment":
                entity = self.nlu_uts.get_period_from_text(NLU_response)
                new_dic = self.nlu_uts.Convert(entity)
                self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

            elif NLU_response["intent"]["name"] == "get_nomina":
                entities = self.nlu_uts.get_entities(NLU_response)
                # print("Entidades: ",entities)
                months = ""
                if len(entities) == 0:
                    new_dic = {"month": month + " " + year}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')
                else:
                    for entity in entities:
                        new_dic = self.nlu_uts.Convert(entity)
                        if entity[0] == "interval":
                            dates = self.nlu_uts.find_dates(new_dic["interval"])
                            # print("DATES: ",dates)
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
                            dates = self.nlu_uts.find_dates(new_dic["month"])
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

            elif NLU_response["intent"]["name"] in ["set_schedule_in", "set_schedule_out", "appointment_with_hour",
                                                    "simple_appointment", "appointment_with_category", "spec_hour"]:
                entities = self.nlu_uts.get_entities(NLU_response)
                print("Intent: ", NLU_response["intent"]["name"])

                if len(entities) > 0:
                    for entity in entities:
                        new_dic = self.nlu_uts.Convert(entity)
                        if entity[0] in ["day", "hour", "minute"]:
                            dates = self.nlu_uts.find_dates(new_dic[entity[0]])
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

                                if (user_date_formated > now) and (
                                        NLU_response["intent"]["name"] not in ["appointment_with_hour",
                                                                               "simple_appointment",
                                                                               "appointment_with_category"]):

                                    user_day_ = [word for word in days if word in NLU_response["text"]]
                                    if entity[0] == "hour":
                                        if len(user_day_) < 1:
                                            delta = user_date_formated - now
                                            real_date = user_date_formated - delta
                                            real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime(
                                                '%d/%m/%Y')
                                            new_dic = {"day": user_hour + " " + real_date}

                                        else:
                                            real_date = user_date_formated - timedelta(days=7)
                                            real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime(
                                                '%d/%m/%Y')
                                            new_dic = {"day": user_hour + " " + real_date}

                                    elif entity[0] == "day":
                                        real_date = user_date_formated - timedelta(days=7)
                                        real_date = datetime.strptime(str(real_date), '%Y-%m-%d %H:%M:%S').strftime(
                                            '%d/%m/%Y')
                                        new_dic = {"day": user_hour + " " + real_date}
                                else:
                                    real_date = datetime.strptime(str(user_date_formated),
                                                                  '%Y-%m-%d %H:%M:%S').strftime(
                                        '%d-%m-%Y')
                                    if user_hour == '00:00:00':
                                        user_hour = '12:00:00'

                                    if NLU_response["intent"]["name"] == "spec_hour":
                                        new_dic = {"hour": user_hour}
                                    else:
                                        new_dic = {"day": user_hour + " " + str(real_date)}

                        elif (entity[0] in ["number"]) and (NLU_response["intent"]["name"] in ["simple_appointment",
                                                                                               "appointment_with_category", "spec_hour"]):

                            if NLU_response["intent"]["name"] == "spec_hour":
                                new_dic = {"hour": str(entity[1])+':00:00'}
                            else:
                                hour = "00:00:00"
                                register = hour + " " + day + "-" + month + "-" + year
                                new_dic = {"day": register}

                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(
                        new_dic).replace("'", '"')

                else:
                    register = hour + " " + day + "/" + month + "/" + year
                    new_dic = {"day": register}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

            elif NLU_response["intent"]["name"] in ["get_schedule_in", "get_schedule_out"]:
                entities = self.nlu_uts.get_entities(NLU_response)
                if len(entities) == 0:

                    register = day + "/" + month + "/" + year
                    new_dic = {"day": register}
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')

                else:
                    for entity in entities:
                        new_dic = self.nlu_uts.Convert(entity)
                        if entity[0] == "day":
                            dates = self.nlu_uts.find_dates(new_dic[entity[0]])
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
                entities = self.nlu_uts.get_entities(NLU_response)

                for entity in entities:
                    new_dic = self.nlu_uts.Convert(entity)
                    if entity[0] == "interval":
                        dates = self.nlu_uts.find_dates(new_dic["interval"])
                        # print("DATES: ", dates)
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
                        # print(new_dic)
                        self.dialog_message["message"] = NLU_response["intent"]["name"] + str(
                            new_dic).replace("'", '"')

                    elif entity[0] == "day":
                        dates = self.nlu_uts.find_dates(new_dic["day"])
                        new_dic["day"] = ""
                        if len(dates) == 1:
                            date = dates[0].split('T')
                            user_date_formated = datetime.strptime(date[0], '%Y-%m-%d')
                            real_date = datetime.strptime(str(user_date_formated), '%Y-%m-%d %H:%M:%S').strftime(
                                '%d/%m/%Y')
                            new_dic["day"] = real_date
                    self.dialog_message["message"] = NLU_response["intent"]["name"] + str(new_dic).replace("'", '"')
        return self.dialog_message

    def post(self, r, sender_id=None):

        if sender_id is not None:
            "TODO TODO TODO TODO"
            "Endpoint to get the ID using the phone number"
            if sender_id == "whatsapp:+34634146030":
                self.user_id = "a.rojas"
            elif sender_id == "whatsapp:+34628088748":
                self.user_id = "i.fernandez"
            else:
                self.user_id = "Undefined user"

        if "message" in r:
            self.nlu_message["text"] = r["message"]
            # print("NLU_message",self.nlu_message)
            NLU_response = requests.post(url=self.NLU_ENDPOINT, json=self.nlu_message)
            dialog_message = self.NLU_adaptation(NLU_response.json())
            dialog_message['sender'] = self.user_id
            # print("Dialog Manager: ",dialog_message)
            dialog_answ = requests.post(url=self.CORE_ENDPOINT, json=dialog_message)

        return dialog_answ.json()
