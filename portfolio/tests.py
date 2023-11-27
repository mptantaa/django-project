from django.test import TestCase
from .models import Portlofios

class PortlofiosModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Portlofios.objects.create(name='Жилой комплекс', unit='23 м2', description='Проверка', image='path/to/image.jpg')

    def test_name_label(self):
        portlofios = Portlofios.objects.get(id=1)
        field_label = portlofios._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Локация')

    def test_unit_label(self):
        portlofios = Portlofios.objects.get(id=1)
        field_label = portlofios._meta.get_field('unit').verbose_name
        self.assertEqual(field_label, 'Метраж')

    def test_description_label(self):
        portlofios = Portlofios.objects.get(id=1)
        field_label = portlofios._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Описание')

    def test_image_label(self):
        portlofios = Portlofios.objects.get(id=1)
        field_label = portlofios._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'Изображение')

    def test_name_max_length(self):
        portlofios = Portlofios.objects.get(id=1)
        max_length = portlofios._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_unit_max_length(self):
        portlofios = Portlofios.objects.get(id=1)
        max_length = portlofios._meta.get_field('unit').max_length
        self.assertEqual(max_length, 15)

    def test_object_name_is_name(self):
        portlofios = Portlofios.objects.get(id=1)
        expected_object_name = f'{portlofios.name}'
        self.assertEqual(expected_object_name, str(portlofios))