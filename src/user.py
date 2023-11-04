from db import conn
import hashlib
from util import buildResponse





def createUser(nombre,email,contraseña,headers):
    try:
        contraseña_bytes = contraseña.encode('utf-8')
        hashed_password = hashlib.blake2b(contraseña_bytes).hexdigest()
        with conn.cursor() as cur:
            sql_string = "INSERT INTO usuarios (nombre_usuario, puntos_usuario, email_usuario, contraseña_usuario) VALUES (%s, 0, %s, %s)"
            cur.execute(sql_string, (nombre, email, hashed_password))

            sql_string = "SELECT * FROM usuarios WHERE email_usuario = %s"
            cur.execute(sql_string, (email,))

        return buildResponse(201,headers,{'message': 'User created: %s' % nombre})
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

def updateUserById(nuevo_nombre, nuevo_email,nueva_contraseña,id,headers):

    contraseña_bytes = nueva_contraseña.encode('utf-8')
    hashed_password = hashlib.blake2b(contraseña_bytes).hexdigest()
    try:
        with conn.cursor() as cur:
            sql_string = "UPDATE usuarios SET nombre_usuario = %s, email_usuario = %s, contraseña_usuario = %s WHERE id_usuario = %s"
            cur.execute(sql_string,(nuevo_nombre,nuevo_email,hashed_password,id))

            sql_string = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cur.execute(sql_string, (id))
            user = cur.fetchone()

            return buildResponse(200,headers,{'message': 'User with id: %s updated' % id,
                                            'user_id':user[0],
                                            'user_email' : user[1],
                                            'username':user[2],
                                            'user_points': user[3]})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})
    
def addPoints(id,points,headers):
    try:
        with conn.cursor() as cur:
            
            sql_string = "UPDATE usuarios SET puntos_usuario = puntos_usuario + %s WHERE id_usuario = %s"
            cur.execute(sql_string, (points,id))
        return buildResponse(201,headers,{'message': '%s Points added to user %s' % (points,id)})
    except Exception as e:
        return buildResponse(500, headers,{'error': str(e)})