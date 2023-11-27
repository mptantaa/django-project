from django.shortcuts import render
from .models import Abouts
# Create your views here.
def index(request):
    about = Abouts.objects.all()
    return render(request, "about/about.html", {'about': about})