import smtplib
import email.utils
from email.mime.text import MIMEText
from smtplib import SMTP as Client


def send_email(sender='author@example.com',   recipient='6142546977@example.com'):
    sender = 'author@example.com'
    recipient = '6142546977@example.com'

    msg = MIMEText('This is the body of the message.')
    msg['To'] = email.utils.formataddr(('Recipient', recipient))
    msg['From'] = email.utils.formataddr(('Author', sender))
    msg['Subject'] = 'Simple test message'

    client = Client('127.0.0.1', 1025)

#   client = smtplib.SMTP('127.0.0.1', 1025)
    client.set_debuglevel(True)  # show communication with the server
    try:
        client.sendmail(sender, [recipient], msg.as_string())
    finally:
        client.quit()
