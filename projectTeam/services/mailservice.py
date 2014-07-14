# -*- coding: UTF-8 -*- 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from projectTeam.powerteamconfig  import *
from jinja2 import Environment, FileSystemLoader


try:
    import thread
except:
    import thread

def send_mail(mail_to,subject,body):
    def _send(mail_to,subject,body):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SMTP_USER
        msg['To'] = mail_to
        content = MIMEText(body, 'html', 'utf-8')
        msg.attach(content)
        try:
            smtp = smtplib.SMTP_SSL()
            smtp.connect(SMTP_HOST)
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.sendmail(SMTP_USER, msg['To'].split(','), msg.as_string())
        except IOError as e:
            print (e)
    if ENABLE_MAIL_NOTICE:
        thread.start_new_thread(_send,(mail_to,subject,body))

def render_mail_template(template_path,**kwargs):
    env = Environment(loader=FileSystemLoader('powerteam/templates/Mail/'))
    template = env.get_template(template_path)
    return template.render(**kwargs)