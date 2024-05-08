# from .IA_services import transcripcion
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from videototext.models import Archivo

from django.conf import settings


def upload_file(request):
    if request.method == "POST" and request.FILES['file']:
        # instancia del modelo Archivo
        archivo_inst = Archivo()

        # guardando en el file system
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # transcribiendo el archivo
        # transcription = transcripcion(f'{settings.BASE_DIR}{uploaded_file_url}')
        # archivo_inst.transcrition = transcription

        # guardando en la base de datos
        archivo_inst.nombre = file.name
        archivo_inst.archivo = uploaded_file_url
        archivo_inst.save()

        return render(request, 'upload-file.html', {
            'uploaded_file_url': uploaded_file_url,
            'uploaded_file_name': filename,
            # 'transcription': transcription)
        })

    return render(request, 'upload-file.html')