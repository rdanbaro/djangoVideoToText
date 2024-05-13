import requests as fetch
from django.shortcuts import render

from videototext.utils.utils import read_config


def upload_file(request):
    if request.method == "POST" and request.FILES['file']:
        # Obteniendo la configuracion
        host, port, api_url = read_config()
        API = f'http://{host}:{port}'
        transcription_api_url = f'{API}/{api_url}'

        # obteniendo el archivo
        file = request.FILES['file']

        # consumiendo la API
        response = fetch.post(
            url=transcription_api_url,
            files={
                'file': file
            },
            headers={
                'Content-Type': 'application/json',
                'Content-Disposition': f'attachment;filename={file.name}'
            }
        )

        data = response.json()

        # response = fetch.get(f'{API}/{read_config("files")}/19')
        #
        # data = response.json()

        return render(request, 'upload-file.html', context={
            'uploaded_file_url': data['archivo'],
            'uploaded_file_name': data['nombre'],
            # 'uploaded_file_storage_name': data['file_storage_name'],
            'transcription': data['transcription'],
            'resumen': data['resumen'],
            'keywords': data['keywords'],
        })

    return render(request, 'upload-file.html')
