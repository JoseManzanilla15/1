from django.db import models
from django.contrib.auth.models import User
from inventario.models import BaseModel


class Conversacion(BaseModel):
    pregunta = models.TextField()
    respuesta = models.TextField()
    temperatura = models.FloatField(default=0.7)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50, default='modelo_base')

    def __str__(self):
        return f"{self.pregunta} - {self.usuario.username}"

    class Meta:
        verbose_name_plural = "Conversación"
        verbose_name = "Conversaciones"
