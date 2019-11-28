#!/usr/bin/python3
import re

class NLU_utils():

    def __init__(self):
        self.extractor = ["CRFEntityExtractor", "DucklingHTTPExtractor"]

    def get_entities(self, NLU_response):
        entities_result = []
        if "entities" in NLU_response:
            entities = NLU_response["entities"]
            for entity in entities:
                tem_vect = []
                if entity['extractor'] == self.extractor[0]:
                    tem_vect.append(entity["entity"])
                    tem_vect.append(entity["value"])
                    entities_result.append(tem_vect)
                elif entity['extractor'] == self.extractor[1]:
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

    def get_period_from_text(self, Response):
        categories = ["mañana", "tarde", "medio dia"]
        if "text" in Response:
            period = [word for word in categories if word in Response["text"]]
            if period:
                return ["period", period[0]]
            else:
                return [None, None]


    def find_dates(self,string):
        return re.findall("\d{4}[-]?\d{1,2}[-]?\d{1,2}[T]\d{1,2}:\d{1,2}:\d{1,2}[.]?\d{1,3}[-]\d{1,2}:\d{1,2}", string)

    def Convert(self, a):
        it = iter(a)
        res_dct = dict(zip(it, it))
        return res_dct
