from django.urls import path
from .views import cargar_archivo, response_form

urlpatterns = [
    path('videototext/', cargar_archivo,name="index"),
    path('response_form/<slug:form>/', response_form ,name="response_form"),
]