from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_html_template(serialized_data):
    create_template(serialized_data)
    sender = "stefenwarner13@gmail.com"
    receiver = serialized_data["email"]
    receivers = ",".join(receiver)
    # receiver = serialized_data["email"]
    message = MIMEMultipart("alternatives")
    message['From'] = sender
    message['Subject'] = "html template"
    message['To'] = receivers
    message['content'] = 'html'
    html_page = r"demo.html"
    with open(html_page, 'r') as html:
        temp = html.read()
    message.attach(MIMEText(temp, 'html'))
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(sender, 'iyutbwcpmhehhmuc')
        mail.send_message(message)
    print("done")   

def create_template(serialized_data):
    file_html = open("demo.html", "w")
    file_html.write('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <h1>{}</h1>
    <body>
        {}
    </body>
    </html>'''.format(serialized_data["subject"], serialized_data["content"]))
    file_html.close()        