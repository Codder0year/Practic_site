# Generated by Django 5.0.7 on 2024-08-27 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='frequency',
            field=models.CharField(choices=[('minute', 'Каждую минуту'), ('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=10),
        ),
    ]
