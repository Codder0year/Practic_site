from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mailsender.models import Mailing


class Command(BaseCommand):
    help = 'Создает группы и назначает права для рассылок'

    def handle(self, *args, **options):
        # Создаем группу для пользователей, которые могут просматривать любые рассылки
        view_all_group, created = Group.objects.get_or_create(name='Просмотр всех рассылок')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Просмотр всех рассылок" создана.'))

        # Назначаем права на просмотр всех рассылок
        can_view_all_permission = Permission.objects.get(codename='can_view_all_mailings')
        view_all_group.permissions.add(can_view_all_permission)

        # Создаем группу для пользователей, которые могут блокировать пользователей сервиса
        block_user_group, created = Group.objects.get_or_create(name='Блокировка пользователей')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Блокировка пользователей" создана.'))

        # Назначаем права на блокировку пользователей
        block_user_permission = Permission.objects.get(codename='block_user')
        block_user_group.permissions.add(block_user_permission)

        # Создаем группу для пользователей, которые могут отключать рассылки
        disable_mailing_group, created = Group.objects.get_or_create(name='Отключение рассылок')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Отключение рассылок" создана.'))

        # Назначаем права на отключение рассылок
        disable_mailing_permission = Permission.objects.get(codename='disable_mailing')
        disable_mailing_group.permissions.add(disable_mailing_permission)

        self.stdout.write(self.style.SUCCESS('Права доступа успешно назначены.'))