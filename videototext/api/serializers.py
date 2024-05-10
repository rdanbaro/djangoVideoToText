from rest_framework import serializers

from videototext.models import Archivo, Keywords


class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = '__all__'


class ArchivoSerializer(serializers.ModelSerializer):
    keywords = KeywordsSerializer(many=False)

    class Meta:
        model = Archivo
        fields = '__all__'

