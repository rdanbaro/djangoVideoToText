from videototext.IA_services import transcripcion
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from videototext.IA_services import palabras_clave
from videototext.funciones_utiles import conversion
from videototext.funciones_utiles import es_video
from django.core.files.storage import FileSystemStorage
from videototext.IA_services import resumen
from rest_framework.generics import ListCreateAPIView


# serializadores
from videototext.api.serializers import KeywordsSerializer, ArchivoSerializer
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
               
                # transcribiendo el archivo
                # transcription = transcripcion(f'{settings.BASE_DIR}{uploaded_file_url}')
                
                
                
                # guardando en la base de datos
                
                
                archivo_inst.nombre = file.name
                archivo_inst.archivo = file
                
                archivo_inst.save()
                
                
                url_definitivo = f'{settings.BASE_DIR}{archivo_inst.archivo.url}'
                if es_video(file):
                    conversion(url_definitivo)
                    #archivo_inst.save()
                    
                    archivo_inst.transcription = transcripcion(url_definitivo)
                else:
                    archivo_inst.transcription = transcripcion(url_definitivo)
                   
            
                archivo_inst.resumen = resumen(archivo_inst.transcription)
                
                keywords_names = palabras_clave(archivo_inst.transcription)
                keywords_instances = []
            
                for name in keywords_names:
                    keyword = Keywords.objects.filter(name=name).first()
                    
                    if keyword is None:
                        keyword = Keywords.objects.create(name=name)
                    keywords_instances.append(keyword)
                archivo_inst.keywords.add(*keywords_instances)
                keywords_data = [{'name': keyword.name} for keyword in archivo_inst.keywords.all()]

                
                data = {
                    'file_id': archivo_inst.id,
                    'file_name': archivo_inst.nombre,
                    'file_storage_name': archivo_inst.archivo.url.split('/')[-1],
                    'file_url': archivo_inst.archivo.url,
                    'transcription': archivo_inst.transcription,
                    'resumen': archivo_inst.resumen,
                    #'keywords': list(archivo_inst.keywords.all()),
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
