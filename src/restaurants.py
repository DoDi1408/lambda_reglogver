from db import conn
from util import buildResponse



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
                    "establishment_id": restaurante[0],
                    "establishment_name": restaurante[1],
                    "establishment_logo": restaurante[2],
                    "establishment_latitud" : restaurante[3],
                    "establishment_longitud" : restaurante[4]
                }
                restaurantes_json.append(restaurante_dict)
            
            return buildResponse(200, headers, restaurantes_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
