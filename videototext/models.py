from django.db import models
from django.conf import settings

# Create your models here.

class Keywords(models.Model):
    name = models.CharField(max_length=255)


class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to=f'{settings.MEDIA_ROOT}')
    transcription = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    keywords = models.ForeignKey(Keywords, on_delete=models.SET_NULL, blank=True, null=True)


