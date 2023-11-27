# Generated by Django 3.2.23 on 2023-11-27 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('a', 'Добавление'), ('e', 'Редактирование'), ('r', 'Удаление'), ('p', 'Опубликовано')], max_length=1, verbose_name='тип действия')),
                ('action_text', models.CharField(blank=True, max_length=50, null=True, verbose_name='действие')),
                ('date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='дата')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('fields_json', models.TextField(blank=True, null=True, verbose_name='значения полей')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Запись истории',
                'verbose_name_plural': 'Записи истории',
                'permissions': (('view_history_entries', 'просмотр истории'),),
                'index_together': {('content_type', 'object_id')},
            },
        ),
    ]
