from django.test import TestCase
from .models import Categories, Prices

class CategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Categories.objects.create(name='Категория 1')
        Categories.objects.create(name='Категория 2')

    def test_name_label(self):
        category = Categories.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название категории')

    def test_name_max_length(self):
        category = Categories.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_name(self):
        category = Categories.objects.get(id=1)
        expected_object_name = f'{category.name}'
        self.assertEqual(expected_object_name, str(category))


class PricesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Категория 1')
        price1 = Prices.objects.create(name='Работа 1', unit='шт.', price=100)
        price2 = Prices.objects.create(name='Работа 2', unit='мм', price=50)
        price1.category.set([category])
        price2.category.set([category])
    def test_name_label(self):
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Наименование работ')

    def test_unit_label(self):
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('unit').verbose_name
        self.assertEqual(field_label, 'Ед. изм.')

    def test_price_label(self):
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'Цена, руб.')

    def test_category_label(self):
        price = Prices.objects.get(id=1)
        field_label = price._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_name_max_length(self):
        price = Prices.objects.get(id=1)
        max_length = price._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_unit_max_length(self):
        price = Prices.objects.get(id=1)
        max_length = price._meta.get_field('unit').max_length
        self.assertEqual(max_length, 5)

    def test_object_name_is_name_and_unit(self):
        price = Prices.objects.get(id=1)
        expected_object_name = f'{price.name}'
        self.assertEqual(expected_object_name, str(price))
