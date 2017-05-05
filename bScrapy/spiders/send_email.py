#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import logging

def send_email(user, pwd, recipient, subject, body, smtp_addr, smtp_port):
    import smtplib

    email_user = user
    email_pwd = pwd

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(smtp_addr, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(email_user, email_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False

def send_email_163(user, pwd, recipient, subject, body):
    smtp_163_addr = "smtp.163.com"
    smtp_163_port = 25
    if send_email(user, pwd, recipient, subject, body, smtp_163_addr, smtp_163_port):
        return True;
    else:
        logging.error ("Send to %s failed." % (recipient))
        return False;
