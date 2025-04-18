from django.urls import path
from .views import Main_view

urlpatterns = [
    path('', Main_view.as_view(), name='main-template')
]