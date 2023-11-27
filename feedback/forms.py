from .models import Feedbacks
from django.forms import ModelForm, TextInput, Textarea

class FeedbacksForm(ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['name', 'phone', 'message']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-group',
                'placeholder': 'Имя'
            }),
            "phone": TextInput(attrs={
                'class': 'form-group',
                'placeholder': 'Телефон'
            }),     
            "message": Textarea(attrs={
                'class': 'form-group',
                'placeholder': 'Сообщение'
            }),          
        }