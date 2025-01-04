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


def get_examine_route(apt_type, apt_category):
	if apt_type == "On-demand":
		if apt_category == "ENT":
			steps = ["Fillout the background check form (Reception area)","General Inspection","Examination of the Ears/Nose and Sinuses/Oral Cavity and Throat/Larynx and Voice","Final Assessment"]
		elif apt_category == "Eyes":
			steps = ["Fillout the background check form (Reception area)","Visual Field Testing","Inspection","Pupil Reactions","Final Assessment"]
		elif apt_category == "Neurology":
			steps = ["Fillout the background check form (Reception area)","Reflexes","Sensory System Examination","Motor System Examination","Final Assessment"]
		else:
			steps = None
	elif apt_type == "General":
		steps = ["Fillout the background check form (Reception area)"," Vital Signs","General Appearance","Head, Neck, and Lymphatic System", "Cardiovascular System", "Respiratory System", "Abdominal Examination", "Skin, Hair, and Nails","Final Assessment"]
		
	elif apt_type == "Driver":
		steps = ["Fillout the background check form (Reception area)"," Vision Test","Cognitive and Mental Health Assessment", "Neurological Examination", "Hearing Test", "Blood Tests (if applicable):","Final Assessment"]
	elif apt_type == "Employment":
		steps = ["Fillout the background check form (Reception area)","General Physical Examination","Vision and Hearing Test", "Neurological Examination", "Respiratory Function Test (if applicable):", "Blood Tests (if applicable):","Final Assessment"]

	else:
		steps = None

	if steps:
		le_string = ""
		for step in steps:
			le_string+=f"<li>{step}</li>"
		examine_route = f"""<ul>{le_string}</ul>"""
		return examine_route