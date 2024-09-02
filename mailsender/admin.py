from django.contrib import admin

# Register your models here.
from .models import Client, Message, Mailing, MailingAttempt

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Mailing)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ['mailing','attempt_date', 'status','server_response']