from django.test import TestCase
from .models import Feedbacks, Contacts

class FeedbacksModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Feedbacks.objects.create(name='Name', phone='+79827272722', message='Message')

    def test_name_label(self):
        feedback = Feedbacks.objects.get(id=1)
        field_label = feedback._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Имя')

    def test_phone_label(self):
        feedback = Feedbacks.objects.get(id=1)
        field_label = feedback._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Телефон')

    def test_message_label(self):
        feedback = Feedbacks.objects.get(id=1)
        field_label = feedback._meta.get_field('message').verbose_name
        self.assertEqual(field_label, 'Сообщение')

    def test_created_at_label(self):
        feedback = Feedbacks.objects.get(id=1)
        field_label = feedback._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'Дата')

    def test_name_max_length(self):
        feedback = Feedbacks.objects.get(id=1)
        max_length = feedback._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_phone_max_length(self):
        feedback = Feedbacks.objects.get(id=1)
        max_length = feedback._meta.get_field('phone').max_length
        self.assertEqual(max_length, 15)

    def test_message_max_length(self):
        feedback = Feedbacks.objects.get(id=1)
        max_length = feedback._meta.get_field('message').max_length
        self.assertEqual(max_length, None)

    def test_object_name_is_name(self):
        feedback = Feedbacks.objects.get(id=1)
        expected_object_name = f'{feedback.name}'
        self.assertEqual(expected_object_name, str(feedback))

class ContactsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contacts.objects.create(name='Name', job='Job', phone='+79127712727', email='test@test.test')

    def test_name_label(self):
        contact = Contacts.objects.get(id=1)
        field_label = contact._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Имя')

    def test_job_label(self):
        contact = Contacts.objects.get(id=1)
        field_label = contact._meta.get_field('job').verbose_name
        self.assertEqual(field_label, 'Должность')

    def test_phone_label(self):
        contact = Contacts.objects.get(id=1)
        field_label = contact._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Телефон')

    def test_email_label(self):
        contact = Contacts.objects.get(id=1)
        field_label = contact._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email')

    def test_name_max_length(self):
        contact = Contacts.objects.get(id=1)
        max_length = contact._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_job_max_length(self):
        contact = Contacts.objects.get(id=1)
        max_length = contact._meta.get_field('job').max_length
        self.assertEqual(max_length, 30)

    def test_phone_max_length(self):
        contact = Contacts.objects.get(id=1)
        max_length = contact._meta.get_field('phone').max_length