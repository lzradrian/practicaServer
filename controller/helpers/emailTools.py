import mimetypes
import smtplib
from email.message import EmailMessage

def send_email(subject,receiverEmail,pdf_path,filename):
    '''
    :param subject:
    :param receiverEmail:
    :param pdf_path:
    :param filename:
    :return:
    '''
    #trimit catre acelasi email pentru test

    gmail_user ='emailpractica10@gmail.com'#emailpractica10@gmail.com'
    gmail_password ='practica123'#'practica123'

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = gmail_user #receiverEmail
    msg.set_content('Hello, this is content')

    # Guess the content type based on the file's extension.
    ctype, encoding = mimetypes.guess_type(pdf_path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(pdf_path, 'rb') as fp:
        msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype,
                           filename=filename)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
    except smtplib.SMTPException:
        raise ValueError("Could not send registration email.")