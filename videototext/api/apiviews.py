from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

# serializadores
from videototext.api.serializers import KeywordsSerializer, ArchivoSerializer
# modelos
from ..models import Keywords, Archivo
# IA Services
#from ..utils.IA_services import resumen, transcripcion, palabras_clave
from ..utils.IA_services import transcripcion
# funciones utiles
from ..utils.media_utils import es_video,es_audio, conversion


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
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        try:
            if 'file' in request.FILES:

                file = request.FILES['file']

                # # validando que sea un audio y transcribiendolo,
                # # if esVideo se convierte y luego se transcribe else se transcribe directamente
                # # start
                if es_video(file):
                    #archivo_inst = conversion(file)
                    #archivo_inst.transcription = transcripcion(archivo_inst.archivo.path)
                elif es_audio(file):
                    archivo_inst = Archivo.objects.create(archivo=file, nombre=file.name)
                    #archivo_inst.transcription = transcripcion(archivo_inst.archivo.path)
                else:
                    archivo_inst = Archivo.objects.create(archivo=file, nombre=file.name)
                    archivo_inst.url = None    
                # end

                # resumiendo la transcripcion del archivo
                #if archivo_inst.transcription is not None:
                #   archivo_inst.resumen = resumen(archivo_inst.transcription)
                #else:
                #   archivo_inst.resumen ='Algo salió mal con la transcripción, intentalo otra vez.'  
                # sacando las palabras claves de la transcripcion del archivo
                #start
                #keywords_names = palabras_clave(archivo_inst.transcription)

                keywords_names = ['name1', 'name dos', 'name Tres']
                keywords_instances = []

                # comprobando si existe la palabra clave en la base de datos sino la crea
                for name in keywords_names:
                    keyword = Keywords.objects.filter(name=name.capitalize()).first()
#
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
                    #'keywords': keywords_data,
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
