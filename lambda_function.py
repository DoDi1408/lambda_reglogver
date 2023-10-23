import sys
import logging
import pymysql
import json
import os
import jwt
import hashlib
from datetime import datetime, timedelta
from custom_encoder import CustomEnconder

# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
        conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    logger.info(event)
    message = event['body']
    if message is None:
        return buildResponse(401,{'message':'mensaje vacio'})
    data = json.loads(message)

    path = event['path']
    httpMethod = event['httpMethod']
    if httpMethod == 'GET' and path == '/health':
        response = buildResponse(200)
    elif httpMethod == 'POST' and path == '/register':

        if 'nombre_usuario' in data and 'email_usuario' in data and 'contraseña_usuario' in data:
            nombre = data['nombre_usuario']
            email = data['email_usuario']
            contraseña = data['contraseña_usuario']
        else:
            return buildResponse(401,{'message' :'Se requieren todos los campos'})
        
        if getUserByEmail(email):
            return buildResponse(401,{'message' :'email ya existe en nuestra base de datos'})
        
        response = createUser(nombre,email,contraseña)

    elif httpMethod == 'POST' and path == '/login':
        email = data['email_usuario']
        contraseña = data['contraseña_usuario']

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT contraseña_usuario FROM usuarios WHERE email_usuario = %s", (email,))
                stored_password_hash = cur.fetchone()
                contraseña_bytes = contraseña.encode('utf-8')
                if stored_password_hash:
                    stored_password_hash = stored_password_hash[0]
                    if hashlib.blake2b(contraseña_bytes).hexdigest() == stored_password_hash:
                        token = generateToken(email)
                        response = buildResponse(200, {'token': token});
                    else:
                        return buildResponse(403,{'message': 'contraseña erronea'})
                else:
                    return buildResponse(403,{'message': 'email no encontrado'})
        except Exception as e:
            return buildResponse(500,{'message': "DB Server Error"})
        
    elif httpMethod == 'POST' and path == '/verify':

        response = buildResponse(200)

    else:
        response = buildResponse(404, {'message': 'Not Found'})
    return response


def buildResponse(statusCode,body=None):
    responseObject = {
        'statusCode' : statusCode,
        'headers':{
            'Content-Type' :'application/json',
            'Access-Control-Allow-Origin' : '*'
        }
    }
    if body is not None:
        responseObject['body'] = json.dumps(body,cls=CustomEnconder)
    return responseObject 

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
        return buildResponse(200,{'message': 'Se ha creado el usuario %s' % nombre})
    except Exception as e:
        return buildResponse(500, {'error': str(e)})
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
        
def generateToken(email):
    if not email:
        return None
    try:
        token_data = {'email': email,'exp': datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(token_data, os.environ['JWT_SECRET'], algorithm='HS256')
        logger.info(token)
    except Exception as e:
        logger.info(e)
        return None
    return token

def verifyToken(email, token):
    try:
        decoded = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        
        if decoded.get('email') == email:
            return {
                'verified': True,
                'message': 'verified'
            }
        else:
            return {
                'verified': False,
                'message': 'invalid user'
            }
    except jwt.ExpiredSignatureError:
        return {
            'verified': False,
            'message': 'token expired'
        }
    except jwt.DecodeError:
        return {
            'verified': False,
            'message': 'invalid token'
        }