# import os
# import django
#
# # Устанавливаем переменную окружения
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
#
# django.setup()
#
# from mailsender.scheduler import start_scheduler
#
# if __name__ == "__main__":
#     start_scheduler()
#     # Чтобы процесс не завершался
#     import time
#     while True:
#         time.sleep(1)