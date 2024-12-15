import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
def send_email(receiver_email, subject, html_content, base64_image=None):
			
	sender_email = os.environ.get('SENDER_EMAIL_USERNAME')
	sender_password = os.environ.get('SENDER_EMAIL_PASSWORD')

	try:
		#Create MIMEMultipart object
		msg = MIMEMultipart("alternative")
		msg["Subject"] = "[BETA-TESTING]" + subject
		msg["From"] = sender_email
		msg["To"] = receiver_email
		# filename = "document.pdf"

		#HTML Message Part
		html = f"""\
			<html>
			<body>
			{html_content}
			</body>
			</html>
			"""

		part = MIMEText(html, "html")
		msg.attach(part)

		if base64_image:
			part = MIMEBase('image', 'png')
			part.set_payload(base64_image)
			
			part.add_header('Content-Transfer-Encoding', 'base64')
			part['Content-Disposition'] = f'attachment; filename="image.png"'
			msg.attach(part)


		# Create secure SMTP connection and send email
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
			server.login(str(sender_email), str(sender_password))
			server.sendmail(sender_email, receiver_email, msg.as_string())
	except Exception as bug:
		print(bug)

