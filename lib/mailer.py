'''

    mailer.py
    fractal

'''

import smtplib

username = "fractalmailer@gmail.com"
password = "redacted"
ssl_port = 465


def send_mail(to_email, message_to_send):
    '''
        sends an email to a user with a message to send
    '''

    server = smtplib.SMTP_SSL('smtp.gmail.com', ssl_port)
    server.login(username, password)
    server.sendmail(
        username,  # from
        to_email,  # to
        message_to_send  # message
    )
    server.quit()


#send_mail("my_email@example.com", "hello world!")
