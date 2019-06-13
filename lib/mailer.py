'''

    mailer.py
    fractal

'''

import smtplib

username = "gabe@ourlol.ca"
password = "pythonlol"
ssl_port = 465


def send_mail(to_email, message_to_send):
    '''
        Sends an email to a user with a message to send.
    '''

    server = smtplib.SMTP_SSL('smtp.gmail.com', ssl_port)
    server.login(username, password)
    server.sendmail(
        username,  # from
        to_email,  # to
        message_to_send  # message
    )
    server.quit()

