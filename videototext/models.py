from django.db import models


# Create your models here.

class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='videototext/')


class Persona(models.Model):
    name = models.CharField(max_length=255)
    img = models.FileField(upload_to='videototext/')
