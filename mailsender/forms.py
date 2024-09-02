from django import forms
from .models import Mailing, Client, Message
from django.utils import timezone


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_date', 'frequency', 'status', 'message', 'clients', 'last_mailing_date']
        widgets = {
            'start_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
            'last_mailing_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
            'clients': forms.CheckboxSelectMultiple(),
            'status': forms.Select(choices=Mailing.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значение по умолчанию для поля start_date
        if not kwargs.get('instance'):
            self.fields['start_date'].initial = timezone.now()
        # Переписываем поле сообщений, чтобы предоставить выбор
        self.fields['message'].queryset = Message.objects.all()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }
