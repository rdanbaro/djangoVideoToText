# from .IA_services import transcripcion
import requests as fetch
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from videototext.utils.utils import read_config


def upload_file(request):
    if request.method == "POST" and request.FILES['file']:

        # Obteniendo la configuracion
        host, port, api_url = read_config()
        API = f'http://{host}:{port}'
        transcription_api_url = f'{API}/{api_url}'
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

        # if es_video(file):
        #     print('Es un video')
        #     clip = mp.VideoFileClip(url_definitivo)
        #     clip.audio.write_audiofile(url_definitivo[:-4] + '.mp3')

        # transcribiendo el archivo y guardando en la variable transcrition
        # archivo_inst.transcrition = transcripcion(url_definitivo)

        api_url_file = read_config('files')
        archivo = fetch.get(url=f'{API}/{api_url_file}/{data["file_id"]}').json()

        inStorage_file_name = archivo['archivo'].split('/')[-1]

        return render(request, 'upload-file.html', {
            'uploaded_file_url': archivo['archivo'],
            'uploaded_file_name': inStorage_file_name,
            # 'file': loaded_file
            # 'transcription': transcription)
        })

    return render(request, 'upload-file.html')