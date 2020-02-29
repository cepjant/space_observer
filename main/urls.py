from django.urls import path
from .views import Main
from django.views.generic import TemplateView

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('map/', TemplateView.as_view(template_name='map.html'), name='map'),
]
