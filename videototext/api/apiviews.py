from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

# IA Services
from videototext.IA_services import palabras_clave
from videototext.IA_services import resumen
from videototext.IA_services import transcripcion
# serializadores
from videototext.api.serializers import KeywordsSerializer, ArchivoSerializer
# funciones utiles
from videototext.funciones_utiles import conversion
from videototext.funciones_utiles import es_video
# modelos
from ..models import Keywords, Archivo


class KeywordsApiView(viewsets.ModelViewSet):
    serializer_class = KeywordsSerializer
    queryset = Keywords.objects.all()


class ArchivoApiView(viewsets.ModelViewSet):
    serializer_class = ArchivoSerializer
    queryset = Archivo.objects.all()


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'file': openapi.Schema(
                type=openapi.TYPE_FILE,
                description='media file'
            ),
        }
    ),
    operation_description='Transcribe, save, and return a media file',
    responses={
        200: openapi.Response("OK", schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        400: "Error de Solicitud"
    }
)
class TransciptionApiView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, format=None):

        try:
            if 'file' in request.FILES:
                archivo_inst = Archivo()

                file = request.FILES['file']

                # guardando en la base de datos
                archivo_inst.nombre = file.name
                archivo_inst.archivo = file

                archivo_inst.save()

                # crea una url valida del fichero
                url_definitivo = f'{settings.BASE_DIR}{archivo_inst.archivo.url}'

                # validando que sea un audio y transcribiendolo,
                # if esVideo se convierte y luego se transcribe else se transcribe directamente
                # start
                if es_video(file):
                    conversion(url_definitivo)

                    archivo_inst.transcription = transcripcion(url_definitivo)
                else:
                    archivo_inst.transcription = transcripcion(url_definitivo)
                # end

                # resumiendo la transcripcion del archivo
                archivo_inst.resumen = resumen(archivo_inst.transcription)

                # sacando las palabras claves de la transcripcion del archivo
                # start
                keywords_names = palabras_clave(archivo_inst.transcription)

                keywords_instances = []

                # comprobando si existe la palabra clave en la base de datos sino la crea
                for name in keywords_names:
                    keyword = Keywords.objects.filter(name=name.capitalize()).first()

                    if keyword is None:
                        keyword = Keywords.objects.create(name=name.capitalize())
                    keywords_instances.append(keyword)

                # asignando las palabras clave al archivo
                archivo_inst.keywords.add(*keywords_instances)

                # obteniendo las palabras claves
                keywords_data = [{'id': keyword.id, 'name': keyword.name} for keyword in archivo_inst.keywords.all()]

                data = {
                    'file_id': archivo_inst.id,
                    'nombre': archivo_inst.nombre,
                    'file_storage_name': archivo_inst.archivo.url.split('/')[-1],
                    'archivo': archivo_inst.archivo.url,
                    'transcription': archivo_inst.transcription,
                    'resumen': archivo_inst.resumen,
                    'keywords': keywords_data,
                }

                return Response(data=data, status=status.HTTP_200_OK)

            else:

                return Response(data={

                    'error': 'No se proporcionó ningún archivo'

                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            return Response(data={

                'error': str(e)

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
