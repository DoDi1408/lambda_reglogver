from db import conn
from util import buildResponse
import json


def getRestaurants():
    with conn.cursor() as cur:
        sql_string = "SELECT * FROM establecimiento"
        cur.execute(sql_string, )
        restaurantes = cur.fetchall()
        return json.dumps(restaurantes)
