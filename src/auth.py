import jwt
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generateToken(email,id,nombre,sourceIp):
    try:
        token_data = {'email': email,'id':id,'nombre':nombre,'sourceIp':sourceIp,'exp': datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(token_data, os.environ['JWT_SECRET'], algorithm='HS256')
    except Exception as e:
        return None
    return token

def authenticateToken(token,sourceIp):
    try:
        ## CAMBIAR os.environ['JWT_SECRET']
        decoded = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        expiration_timestamp = decoded.get('exp', 0)  # Obtiene el tiempo de expiración del token
        email = decoded.get('email')
        id = decoded.get('id')
        nombre = decoded.get('nombre')
        tokenIp = decoded.get('sourceIp')
        if sourceIp == tokenIp:
            # Verifica si el token está a punto de expirar (menos de 30 minutos restantes)
            current_time = datetime.now().timestamp()
            if expiration_timestamp - current_time < 1800:
                # Crea un nuevo token con el mismo email
                token_data = {'email': email,'id':id,'nombre':nombre,'sourceIp':sourceIp,'exp': current_time + 3600}
                new_token = jwt.encode(token_data, os.environ['JWT_SECRET'], algorithm='HS256')
                return {
                'verified': True,
                'message': 'verified',
                'accessToken' : new_token,
                'email' : email,
                'id' : id,
                'nombre' : nombre
                }
            else:
                return {
                    'verified': True,
                    'message': 'verified',
                    'accessToken' : token,
                    'email' : email,
                    'id' : id,
                    'nombre' : nombre
                    }
        else:
            return{
                'verified' : False,
                'message' : 'Ip Not Valid',
                'accessToken' : token
            }
    except jwt.ExpiredSignatureError:
        return {
            'verified': False,
            'message': 'Token Expired',
            'accessToken' : token
        }
    except jwt.DecodeError:
        return {
            'verified': False,
            'message': 'Invalid Token',
            'accessToken' : token
        }