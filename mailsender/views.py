from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import MailingForm
from .models import Mailing, Client, Message
from django.utils import timezone

###########Рассылка##################
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailsender/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailsender/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailsender/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailsender:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'GET' and not self.object:
            form.fields['start_date'].initial = timezone.now()
        return form

    def form_valid(self, form):
        if Mailing.objects.filter(start_date=form.cleaned_data['start_date'], message=form.cleaned_data['message']).exists():
            form.add_error(None, "Рассылка с таким сообщением уже существует.")
            return self.form_invalid(form)
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['messages'] = Message.objects.all()
        context['clients'] = Client.objects.all()
        context['statuses'] = Mailing.STATUS_CHOICES
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailsender/mailing_form.html'
    fields = ['start_date', 'frequency', 'status', 'message', 'clients']
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailsender/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailsender:mailing_list')


###########Клиенты##################
class ClientListView(ListView):
    model = Client
    template_name = 'mailsender/client_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailsender/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(CreateView):
    model = Client
    template_name = 'mailsender/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailsender:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'mailsender/client_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailsender:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailsender/client_confirm_delete.html'
    success_url = reverse_lazy('mailsender:client_list')


###########Сообщения##################
class MessageListView(ListView):
    model = Message
    template_name = 'mailsender/message_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailsender/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailsender/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailsender:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailsender/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailsender:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailsender/message_confirm_delete.html'
    success_url = reverse_lazy('mailsender:message_list')