from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField('Название категории', max_length=50, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        
class Prices(models.Model):
    name = models.CharField('Наименование работ', max_length=50, default='')
    unit = models.CharField('Ед. изм.', max_length=5, default='')
    price = models.IntegerField('Цена, руб.')
    category = models.ManyToManyField(Categories, verbose_name='Категория')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


