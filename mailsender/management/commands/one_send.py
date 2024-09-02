import smtplib
from django.core.mail import send_mail
from django.core.management import BaseCommand
from config import settings
from mailsender.models import Mailing, MailingAttempt


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status='started')

        print(f"Checking mailings with status 'scheduled'")

        for mailing in mailings:
            print(f"Processing mailing: {mailing.id}")

            clients = mailing.clients.all()

            for client in clients:

                try:
                    print(f"Sending email to {client.email}")

                    response = send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )

                    MailingAttempt.objects.create(
                        mailing=mailing,
                        client=client,
                        server_response=response,
                        status='sent'
                    )
                    print(f"Email sent to {client.email}")

                except smtplib.SMTPException as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        client=client,
                        server_response=str(e),
                        status='failed'
                    )

                    print(f"Error sending email to {client.email}: {e}")