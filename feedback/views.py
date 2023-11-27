from django.shortcuts import render, redirect
from .forms import FeedbacksForm
from .models import Contacts

# Create your views here.
def feedback(request):
    error = ''
    if request.method == 'POST':
        form = FeedbacksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else: 
            error = 'Ошибка при заполнении'
    form = FeedbacksForm
    contacts = Contacts.objects.all()
    return render(request, 'feedback/feedback.html', {'form': form, 'error': error, 'contacts': contacts})