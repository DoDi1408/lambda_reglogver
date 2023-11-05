import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


remitente = "bamxa535@gmail.com"
verification_link = f"https://tf0mj1svb3.execute-api.us-east-2.amazonaws.com/prod/verify?token={token}"

email_body = f"""<pre>
Bienvenido! Tu cuenta ha sido creada.
<a href="{verification_link}">Haz click aquí para verificar tu cuenta</a>
Gracias,
Equipo BAMX Rewards.
</pre>"""

msg = MIMEMultipart()
msg['From'] = remitente
msg['To'] = destinatario
msg['Subject'] = 'simple email in python'
msg.attach(MIMEText(email_body, 'html'))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.ehlo()
server.login(remitente, "xtjvuhwqejgktccb")
server.sendmail(remitente, destinatario, msg.as_string())
server.quit()