from django.db import models


# Create your models here.
class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Клиенты"
        verbose_name = "Клиент"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Сообщения"
        verbose_name = "Сообщение"


class Mailing(models.Model):
    FREQUENCY_CHOICES = [
        ('minute', 'Каждую минуту'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_date = models.DateTimeField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    last_mailing_date = models.DateTimeField(default=None, null=True, blank=True)
    # first_mailing_date = models.DateTimeField(default=None)
    # next_mailing_date = models.DateTimeField(default=None)

    def __str__(self):
        return f"Рассылка {self.pk} - {self.status}"

    class Meta:
        verbose_name_plural = "Рассылки"
        verbose_name = "Рассылка"
        permissions = [
            ("can_view_all_mailings", "Может просматривать любые рассылки"),
            ("block_user", "Может блокировать пользователей сервиса"),
            ("disable_mailing", "Может отключать рассылки"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Попытка {self.pk} - {self.status}"

    class Meta:
        verbose_name_plural = "Попытки рассылки"
        verbose_name = "Попытка рассылки"
