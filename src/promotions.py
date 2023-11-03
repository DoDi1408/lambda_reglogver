from db import conn
from util import buildResponse



def getRestaurantPromotions(id_restaurant,headers):
    try:
        with conn.cursor() as cur:
            sql_string = "SELECT * FROM promocion WHERE id_establecimiento = %s"
            cur.execute(sql_string, (id_restaurant))
            promos = cur.fetchall()
            # Construir una lista de diccionarios en el formato deseado
            promos_json = []
            for promo in promos:
                promo_dict = {
                    "id_establecimiento": promo[0],
                    "id_promocion": promo[1],
                    "nombre": promo[2],
                    "imagen" : promo[3],
                    "texto_descriptivo" : promo[4],
                    "costo" : promo[5]
                }
                promos_json.append(promo_dict)
            return buildResponse(200, headers, promos_json)
    except Exception as e:
        return e
    
def getPromotions(headers):
    try:
        with conn.cursor() as cur:
            sql_string = "SELECT * FROM promocion"
            cur.execute(sql_string, )
            promos = cur.fetchall()
            # Construir una lista de diccionarios en el formato deseado
            promos_json = []
            for promo in promos:
                promo_dict = {
                    "id_establecimiento": promo[0],
                    "id_promocion": promo[1],
                    "nombre": promo[2],
                    "imagen" : promo[3],
                    "texto_descriptivo" : promo[4],
                    "costo" : promo[5]
                }
                promos_json.append(promo_dict)
            return buildResponse(200, headers, promos_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
