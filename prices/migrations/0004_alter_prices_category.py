# Generated by Django 3.2.19 on 2023-07-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0003_auto_20230628_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='category',
            field=models.ManyToManyField(to='prices.Categories', verbose_name='Категория'),
        ),
    ]
