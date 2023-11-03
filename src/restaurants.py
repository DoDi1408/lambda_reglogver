from db import conn
from util import buildResponse
import json


def getRestaurants(headers):
    try:
        with conn.cursor() as cur:
            sql_string = "SELECT * FROM establecimiento"
            cur.execute(sql_string, )
            restaurantes = cur.fetchall()
            # Construir una lista de diccionarios en el formato deseado
            restaurantes_json = []
            for restaurante in restaurantes:
                restaurante_dict = {
                    "id": restaurante[0],
                    "nombre": restaurante[1],
                    "logo": restaurante[2],
                    "latitud" : restaurante[3],
                    "longitud" : restaurante[4]
                    # Agrega otros campos aquí según sea necesario
                }
                restaurantes_json.append(restaurante_dict)
            
            return buildResponse(200, headers, restaurantes_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})