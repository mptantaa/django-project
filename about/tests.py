from django.test import TestCase
from .models import Abouts

class AboutsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Abouts.objects.create(title='Заголовок', about_text='Текст')

    def test_abouts_title(self):
        abouts = Abouts.objects.get(id=1)
        field_title = abouts._meta.get_field('title').verbose_name
        self.assertEquals(field_title, 'Заголовок')

    def test_abouts_about_text(self):
        abouts = Abouts.objects.get(id=1)
        field_about_text = abouts._meta.get_field('about_text').verbose_name
        self.assertEquals(field_about_text, 'Текст')

    def test_abouts_str(self):
        abouts = Abouts.objects.get(id=1)
        expected_str = abouts.about_text
        self.assertEquals(str(abouts), expected_str)