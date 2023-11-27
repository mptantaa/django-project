# Generated by Django 3.2.19 on 2023-07-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portlofios_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='portlofios',
            name='description',
            field=models.TextField(default='', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='portlofios',
            name='image',
            field=models.ImageField(upload_to='static/img/', verbose_name='Изображение'),
        ),
    ]