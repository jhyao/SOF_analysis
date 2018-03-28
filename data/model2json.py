from json import JSONDecoder, JSONEncoder
from .models import json_model

class ModelEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, json_model.JSONModel):
            return o.get_data()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


class ModelDecoder(JSONDecoder):

    def hook():
        pass
    
