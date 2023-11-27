from django.urls import path
from . import views


urlpatterns = [
    path('', views.portfolio, name="portfolio"),
    path('<int:object_id>', views.portfolio_detail, name='portfolio'),
]
