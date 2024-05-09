from rest_framework import viewsets

# modelos
from videototext.models import Keywords, Archivo

# serializadores
from videototext.api.serializers import KeywordsSerializer, ArchivoSerializer


class KeywordsApiView(viewsets.ModelViewSet):
    serializer_class = KeywordsSerializer
    queryset = Keywords.objects.all()


class ArchivoApiView(viewsets.ModelViewSet):
    serializer_class = ArchivoSerializer
    queryset = Archivo.objects.all()


