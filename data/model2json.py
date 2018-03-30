from json import JSONDecoder, JSONEncoder
from .models import json_model
import datetime

class ModelEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, json_model.JSONModel):
            return o.get_data()
        if isinstance(o, datetime.datetime):
            return int(o.timestamp())
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


class ModelDecoder(JSONDecoder):

    def hook():
        pass
    
