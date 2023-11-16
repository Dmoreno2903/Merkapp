from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Supermercado(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)
    latitud = models.CharField(max_length=50)
    longitud = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.nombre
    

class Mercado(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=50)
    costo = models.IntegerField(blank=False)
    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)