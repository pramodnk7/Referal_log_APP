import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from .passcode import passcode


def send_mail(subject, body, receiver_email):
	try:
	#The mail addresses and password
		sender_address = "pramodnk7@gmail.com"
		sender_pass = "trytfpevptvulymf"
		receiver_address = receiver_email
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_email
		message['Subject'] = subject   #The subject line
		message.attach(MIMEText(body, 'html'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
		session.starttls() #enable security
		session.login(sender_address, sender_pass) #login with mail_id and password
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
		print('Mail Sent', flush=True)
	except Exception as e:
		print(e, flush=True)