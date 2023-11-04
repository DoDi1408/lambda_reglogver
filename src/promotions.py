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
                    "establishment_id": promo[0],
                    "promotion_id": promo[1],
                    "promotion_name": promo[2],
                    "promotion_image" : promo[3],
                    "promotion_descriptive_text" : promo[4],
                    "promotion_price" : promo[5]
                }
                promos_json.append(promo_dict)
            return buildResponse(200, headers, promos_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
    
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
                    "establishment_id": promo[0],
                    "promotion_id": promo[1],
                    "promotion_name": promo[2],
                    "promotion_image" : promo[3],
                    "promotion_descriptive_text" : promo[4],
                    "promotion_price" : promo[5]
                }
                promos_json.append(promo_dict)
            return buildResponse(200, headers, promos_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
