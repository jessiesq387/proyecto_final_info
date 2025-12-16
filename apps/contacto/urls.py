from django.urls import path
from .views import ContactoUsuario

urlpatterns = [
    path('contacto/', ContactoUsuario.as_view(), name='contacto'),
]