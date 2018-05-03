from json import JSONDecoder, JSONEncoder
import datetime

class ModelEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, 'get_data'):
            return o.get_data()
        if isinstance(o, datetime.datetime):
            return int(o.timestamp())
        if isinstance(o, set):
            return list(o)
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)


class ModelDecoder(JSONDecoder):

    def hook(self):
        pass
    
