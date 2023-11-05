from email.message import EmailMessage
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from user import setUserVerified
import os
import jwt
import smtplib

def sendVerificationEmail(destinatario,token):
    remitente = "bamxa535@gmail.com"

    verification_link = f"https://tf0mj1svb3.execute-api.us-east-2.amazonaws.com/prod/verify?token={token}"

    email_body = f"""<pre>
    Bienvenido! Tu cuenta ha sido creada.
    <a href="{verification_link}">Haz click aquí para verificar tu cuenta</a>
    Gracias,
    Equipo BAMX Rewards.
    </pre>"""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(remitente, os.environ['GMAIL_SECRET'])
    server.sendmail(remitente, destinatario, msg="Subject: Test\n\n This is a test from lambda")
    server.close()
    #msg = MIMEText(email_body ,'html')


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
        if sourceIp == tokenIp:
            setUserVerified(email)
        else:
            return{
                'verified' : False,
                'message' : 'Ip Not Valid',
            }
    except jwt.ExpiredSignatureError:
        return {
            'verified': False,
            'message': 'Token Expired',
        }
    except jwt.DecodeError:
        return {
            'verified': False,
            'message': 'Invalid Token',
        }