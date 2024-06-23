from smtplib import SMTPException
from django.core.mail import send_mail

from visota.celery import app


@app.task(bind=True)
def pass_request_to_email(self, subject, message):
        try:
            send_mail(
                subject,
                message,
                'info@visota13.ru',
                ['info@visota13.ru'],
                fail_silently=False
                )
        except SMTPException as e:
            raise self.retry(exc=e, countdown=2*60)