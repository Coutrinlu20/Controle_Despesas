
from django.urls import path, include
from usuario.views import home

urlpatterns = [
    path('', home),
]