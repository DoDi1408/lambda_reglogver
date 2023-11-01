from db import conn
import hashlib
from util import buildResponse
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

#default headers:
headers = {
            'Content-Type' :'application/json',
            'Access-Control-Allow-Origin' : '*'
}

def createUser(nombre,email,contraseña):
    try:
        contraseña_bytes = contraseña.encode('utf-8')
        hashed_password = hashlib.blake2b(contraseña_bytes).hexdigest()
        with conn.cursor() as cur:
            sql_string = "INSERT INTO usuarios (nombre_usuario, puntos_usuario, email_usuario, contraseña_usuario) VALUES (%s, 0, %s, %s)"
            cur.execute(sql_string, (nombre, email, hashed_password))
            conn.commit()

            sql_string = "SELECT * FROM usuarios WHERE email_usuario = %s"
            cur.execute(sql_string, (email,))

            logger.info("The following items have been added to the database:")
            logger.info(cur)
        return buildResponse(200,headers,{'message': 'Se ha creado el usuario %s' % nombre})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
    #tratar errores

def getUserByEmail(email):
    with conn.cursor() as cur:
        sql_string = "SELECT * FROM usuarios WHERE email_usuario = %s"
        cur.execute(sql_string, (email,))
        user = cur.fetchone()
        if user:
            return user
        else:
            return None

def updateUserByEmail(nuevo_nombre, nuevos_puntos,nueva_contraseña,email):
    try:
        with conn.cursor() as cur:
            sql_string = "UPDATE usuarios SET nombre_usuario = %s, puntos_usuario = %s, contraseña_usuario = %s WHERE email_usuario = %s"
            cur.execute(sql_string,(nuevo_nombre,nuevos_puntos,nueva_contraseña,email))
            conn.commit()
            return buildResponse(200,headers,{'message': 'Se ha actualizado el usuario %s' % nuevo_nombre})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})