from django.apps import AppConfig


class MailsenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailsender'

    # def ready(self):
    #     from . import services
    #     services.start_scheduler()
