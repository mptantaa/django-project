# Generated by Django 3.2.19 on 2023-06-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20230625_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Антон', max_length=30, verbose_name='Имя')),
                ('job', models.CharField(default='Директор', max_length=30, verbose_name='Должность')),
                ('phone', models.CharField(default='+79000000000', max_length=15, verbose_name='Телефон')),
                ('email', models.CharField(default='anton@anton.ru', max_length=40, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]