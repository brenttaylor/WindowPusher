import smtplib
from email.mime.text import MIMEText
import fls


class FLSMailException(Exception):
    pass


message = fls.struct(to="", sender="", subject="", body="")
mail_settings = fls.struct(username="", password="", smtp_server="smtp.gmail.com",
                           smtp_port=587, tls=True, ssl=False)


def send_mail(mail, settings):
    server = None
    msg = MIMEText(mail.body)
    msg["Subject"] = mail.subject
    msg["To"] = mail.to
    msg["From"] = mail.sender

    try:
        if not settings.ssl:
            server = smtplib.SMTP(settings.smtp_server,
                                  settings.smtp_port)
            if settings.tls:
                server.starttls()
        else:
            server = smtplib.SMTP_SSL(settings.smtp_server,
                                      settings.smtp_port)
        server.login(settings.username, settings.password)
        server.sendmail(settings.username, mail.to,
                        msg.as_string())

    except smtplib.SMTPConnectError:
        raise FLSMailException("Could not connect to the SMTP server.\n")
    except smtplib.SMTPServerDisconnected:
        raise FLSMailException("The remote server hung up unexpectedly.  Please try again.\n")
    except smtplib.SMTPSenderRefused:
        raise FLSMailException("Sender address refused.\n")
    except smtplib.SMTPRecipientsRefused:
        raise FLSMailException("Recipient refused.\n")
    except smtplib.SMTPDataError:
        raise FLSMailException("Message data refused.\n")
    except smtplib.SMTPHeloError:
        raise FLSMailException("There was a problem communicating with the server.  Please try again.\n")
    except smtplib.SMTPAuthenticationError:
        raise FLSMailException("Username/Password refused by the server.  Wrong username or password.\n")
    except:
        raise FLSMailException("Could not connect to server.  Are your settings correct?")
    finally:
        try:
            if server is not None:
                server.quit()
        except smtplib.SMTPServerDisconnected:
            pass