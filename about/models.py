from django.db import models

# Create your models here.

class Abouts(models.Model):
    title = models.CharField('Заголовок', max_length=60, default='')
    about_text = models.TextField('Текст')

    def __str__(self):
        return self.about_text

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'