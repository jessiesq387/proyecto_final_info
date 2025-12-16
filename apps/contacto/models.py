from django.db import models
from django.utils import timezone


class Contacto(models.Model):
    nombre_apellido = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=30)
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre_apellido
