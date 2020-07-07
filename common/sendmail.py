import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from loguru import logger
from pathlib import Path

MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_CC = os.getenv("MAIL_CC")
MAIL_SUBJECT = os.getenv("MAIL_SUBJECT")
MAIL_SMTP_HOST = os.getenv("MAIL_SMTP_HOST")
MAIL_SMTP_PORT = os.getenv("MAIL_SMTP_PORT")
MAIL_SMTP_LOGIN = os.getenv("MAIL_SMTP_LOGIN")


def send_mail(name: str, email: str, pdf_filepath: str, smtp_password: str):
    body = f"""
    <p>
        Bonjour {name.capitalize()},
    </p>
    <p>
        Veuillez trouver ci-joint la facture correspondant à votre adhésion au club du <b>SJB pour la saison 
2020/2021</b>. 
    </p>
    <p>Cordialement,
        <br/>le SJB
    </p>
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message.attach(MIMEText(body, "html"))
    message["From"] = MAIL_SENDER
    message["To"] = email
    message["Subject"] = MAIL_SUBJECT
    message["cc"] = MAIL_CC
    message["reply-to"] = MAIL_SENDER

    # Open PDF file in binary mode
    with open(pdf_filepath, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    filename = Path(pdf_filepath).name
    logger.info(f"Add {filename} as an attachment")
    # Add header as key/value pair to attachment part
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    # Add attachment to message and convert message to string
    message.attach(part)

    text = message.as_string()

    # Log in to server using secure context and send email
    with SMTP_SSL(MAIL_SMTP_HOST, MAIL_SMTP_PORT) as server:
        server.login(MAIL_SMTP_LOGIN, smtp_password)
        server.sendmail(MAIL_SENDER, [email, MAIL_CC], text)
        logger.info(f"Successfully sent email to {email}")
