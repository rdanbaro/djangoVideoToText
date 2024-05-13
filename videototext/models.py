from django.db import models
from django.conf import settings


# Create your models here.

class Keywords(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='files/in_DB')
    transcription = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    keywords = models.ManyToManyField(Keywords, blank=True)

    def __str__(self):
        return self.archivo.url.split('/')[-1]
