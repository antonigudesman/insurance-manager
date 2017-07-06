import sendgrid
from sendgrid.helpers.mail import *

def send_email(from_email, subject, to_email, content):
    sg = sendgrid.SendGridAPIClient(apikey='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')

    from_email = Email(from_email, "Benchmark")
    to_email = Email(to_email)

    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())
