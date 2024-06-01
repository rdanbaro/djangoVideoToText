import requests as fetch
from django.shortcuts import render

from videototext.utils.utils import read_config
import logging

logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == "POST" and 'file' in request.FILES:
        try:
            # Obteniendo la configuración
            host, api_url = read_config()
            transcription_api_url = f'{host}/{api_url}'
            logger.info(f'URL de la API: {transcription_api_url}')
            
            # Obteniendo el archivo
            file = request.FILES['file']
            logger.info(f'Nombre del archivo: {file.name}, Tamaño: {file.size}')

            # Consumiendo la API
            response = fetch.post(
                url=transcription_api_url,
                files={'file': (file.name, file.read(), file.content_type)},
                headers={'Content-Disposition': f'attachment;filename={file.name}'}
            )

            response.raise_for_status()  # Lanzar error para códigos de estado HTTP 4xx/5xx
            logger.info(f'Respuesta de la API: {response.status_code}, {response.text}')

            data = response.json()

            return render(request, 'upload-file.html', context={
                'uploaded_file_url': data.get('archivo', ''),
                'uploaded_file_name': data.get('nombre', ''),
                'transcription': data.get('transcription', ''),
                'resumen': data.get('resumen', ''),
            })
        except fetch.RequestException as e:
            logger.error(f'Error en la solicitud: {e}')
            return JsonResponse({'error': 'Error al comunicarse con el servidor de transcripción'}, status=500)
        except ValueError as e:
            logger.error(f'Error al procesar la respuesta JSON: {e}')
            return JsonResponse({'error': 'Respuesta inválida del servidor de transcripción'}, status=500)
        except Exception as e:
            logger.error(f'Error inesperado: {e}')
            return JsonResponse({'error': 'Ocurrió un error inesperado'}, status=500)

    return render(request, 'upload-file.html')
