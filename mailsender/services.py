from django.core.mail import send_mail
from django.utils import timezone
from mailsender.models import Mailing, MailingAttempt, Client
from django.conf import settings


def send_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(start_date__lte=now, status='started')

    print(f"Checking mailings at {now}")

    for mailing in mailings:
        if mailing.last_mailing_date:
            mailing.status = 'completed'
            mailing.save()

        print(f"Processing mailing: {mailing.id}")

        clients = mailing.clients.all()

        for client in clients:
            try:
                print(f"Sending email to {client.email}")

                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                MailingAttempt.objects.create(
                    mailing=mailing,
                    client=client,
                    attempt_date=now,
                    server_response='Email sent successfully',
                    status='sent'
                )
                print(f"Email sent to {client.email}")

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    client=client,
                    attempt_date=now,
                    server_response=str(e),
                    status='failed'
                )
                print(f"Error sending email to {client.email}: {e}")