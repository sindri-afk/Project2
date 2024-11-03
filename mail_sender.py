import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

class EmailSender:
    def send_email(self):
        message = Mail(
            from_email=os.environ.get('SENDGRID_SENDER_MAIL'),
            to_emails='',
            subject='',
            html_content='')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)