from django.db import models

# Create your models here.
class Portlofios(models.Model):
    name = models.CharField('Локация', max_length=50, default='')
    unit = models.CharField('Метраж', max_length=15, default='')
    description = models.TextField('Описание', default='')
    image = models.ImageField(upload_to='static/img/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'

