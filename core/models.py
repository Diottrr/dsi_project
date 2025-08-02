from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pregunta_secreta = models.CharField(max_length=255)
    respuesta_secreta = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
