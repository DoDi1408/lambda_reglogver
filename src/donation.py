from db import conn
from util import buildResponse

def getDonationsByUserId(id,headers):
    try:
        with conn.cursor() as cur:
            sql_string = "SELECT * FROM donacion WHERE id_usuario = %s"
            cur.execute(sql_string, (id))
            donaciones = cur.fetchall()
            # Construir una lista de diccionarios en el formato deseado
            donaciones_json = []
            for donacion in donaciones:
                promo_dict = {
                    "user_id": donacion[0],
                    "donation_id": donacion[1],
                    "donation_date": donacion[2].strftime('%Y-%m-%d'),
                    "donation_quantity" : donacion[3],
                }
                donaciones_json.append(promo_dict)
            return buildResponse(200, headers, donaciones_json)
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
    
def createDonation(id,amount,headers):
    try:
        with conn.cursor() as cur:
            sql_string = "INSERT INTO donacion (id_usuario, fecha, cantidad) VALUES (%s, CURRENT_TIMESTAMP(), %s)"
            cur.execute(sql_string, (id,amount))
            return buildResponse(200, headers, {'message' : 'Success'})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
    