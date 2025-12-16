from django.urls import path
from .views import ContactoUsuario
from .views import acerca_de_nosotros

urlpatterns = [
    path('contacto/', ContactoUsuario.as_view(), name='contacto'),
    path('acerca-de-nosotros/', acerca_de_nosotros, name='acerca_de_nosotros'),
]


