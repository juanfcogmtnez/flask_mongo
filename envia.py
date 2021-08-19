import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send(diremail,direccion):
	direccion = str(direccion)
	direccion = direccion[2:-1]
	direccion = direccion+"/repwd/"+diremail
	sender_email = "desarrollos.simalga@gmail.com"
	receiver_email = diremail
	password = "Jfgm_4778"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Reset password"
	message["From"] = sender_email
	message["To"] = receiver_email

	# Create the plain-text and HTML version of your message
	html = """\
	<html>
	  <body>
		<p>Hola,<br><br>
		   <a href="""+direccion+"""'>Haz click para generar una nueva contraseña</a> 
		</p>
	  </body>
	</html>
	"""

	# Turn these into plain/html MIMEText objects
	part1 = MIMEText(html, "html")

	# Add HTML/plain-text parts to MIMEMultipart message
	# The email client will try to render the last part first
	message.attach(part1)

	# Create secure connection with server and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)
	return "Te hemos enviado un email para resetear la contraseña"
