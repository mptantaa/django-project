from django.db import models

# Create your models here.

class Feedbacks(models.Model):
    name = models.CharField('Имя', max_length=30, default='')
    phone = models.CharField('Телефон', max_length=15, default='')
    message = models.TextField('Сообщение', default='')
    created_at = models.DateTimeField('Дата', auto_now_add=True,)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

class Contacts(models.Model):
    name = models.CharField('Имя', max_length=30, default='Антон')
    job = models.CharField('Должность', max_length=30, default='Директор')
    phone = models.CharField('Телефон', max_length=15, default='+79000000000')
    email = models.CharField('Email', max_length=40, default='anton@anton.ru')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'