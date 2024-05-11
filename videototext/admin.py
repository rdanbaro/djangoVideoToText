from django.contrib import admin

# Register your models here.
from videototext.models import Archivo, Keywords

admin.site.register(Archivo)
admin.site.register(Keywords)
