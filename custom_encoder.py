import json
from decimal import Decimal
from typing import Any

class CustomEnconder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,Decimal):
            return float(obj)
        return json.JSONEncoder.default(self,obj)