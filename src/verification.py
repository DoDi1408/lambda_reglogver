from datetime import datetime, timedelta
import logging
from user import setUserVerified
import os
import jwt
import boto3

# Create an SES client
ses_client = boto3.client('ses',region_name='us-east-2')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def sendVerificationEmail(receiver,token):
    try:
        sender = "bamxa535@gmail.com" 

        verification_link = f"https://tf0mj1svb3.execute-api.us-east-2.amazonaws.com/prod/verify?token={token}"

        email_body = f"""<pre>
        Bienvenido! Tu cuenta ha sido creada.
        <a href="{verification_link}">Haz click aquí para verificar tu cuenta</a>
        Gracias,
        Equipo BAMX Rewards.
        </pre>"""

        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [receiver]},
            Message={
                'Subject': {'Charset': 'UTF-8','Data': 'An Interesting Title'},
                'Body': {'Html': {'Data': email_body}}
            }
        )

    except Exception as e:
        logger.error(f"Error al enviar el correo electrónico de verificación: {str(e)}")


def createVerifyToken(email,sourceIp):
    try:
        token_data = {'email':email,'sourceIp':sourceIp,'exp': datetime.utcnow() + timedelta(hours=6)}
        token = jwt.encode(token_data, os.environ['JWT_SECRET'], algorithm='HS256')
    except Exception as e:
        return None
    return token

def verifyEmail(token,sourceIp):
    try:
        decoded = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        email = decoded.get('email')
        tokenIp = decoded.get('sourceIp')
        logger.info(email)
        logger.info(tokenIp)
        if sourceIp == tokenIp:
            logger.info("LA IP ES LA MISMA")
            setUserVerified(email)
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False