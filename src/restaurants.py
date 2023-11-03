from db import conn
from util import buildResponse
import json


def getRestaurants(headers):
    try:
        with conn.cursor() as cur:
            sql_string = "SELECT * FROM establecimiento"
            cur.execute(sql_string, )
            restaurantes = cur.fetchall()
            return buildResponse(200,headers,{json.dumps(list(restaurantes))})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})