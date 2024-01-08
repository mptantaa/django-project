"""
URL configuration for agent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from portfolio.views import PortfoliosViewSet
from prices.views import PricesViewSet, CategoriesViewSet
from feedback.views import FeedbacksViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'portfolio', PortfoliosViewSet, basename='portfolios')
router.register(r'prices', PricesViewSet, basename='prices')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'feedbacks', FeedbacksViewSet, basename='feedbacks')

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls'), name="about"),
    path('feedback/', include('feedback.urls'), name="feedback"),
    path('prices/', include('prices.urls'), name="prices"),
    path('portfolio/', include('portfolio.urls'), name="portfolio"),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
