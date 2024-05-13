import mimetypes
import uuid

import moviepy.editor as mp
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from videototext.models import Archivo


def es_video(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('video/') and tipo_mime != 'video/m4a'


def es_audio(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('audio/')


def conversion(file):
    # Guarda el archivo en la carpeta de medios
    fs = FileSystemStorage()
    unique_id = str(uuid.uuid4())
    video_filename = fs.save(f'files/{unique_id}_{file.name}', file)
    video_path = fs.path(video_filename)

    # Crea un objeto VideoFileClip
    video_clip = mp.VideoFileClip(video_path)

    # Extrae el audio del clip de video
    audio_clip = video_clip.audio

    # Define la ruta para el archivo de audio (cambia la extensión si lo deseas)
    audio_relative_path = video_filename[:-4] + '.mp3'
    audio_absolute_path = video_path[:-4] + '.mp3'

    # Guarda el archivo de audio utilizando FileSystemStorage
    audio_clip.to_audiofile(audio_absolute_path)

    with open(audio_absolute_path, 'rb') as audio_file:
        audio_file_name = audio_relative_path.split('/')[1]
        content = ContentFile(
            audio_file.read(),
            name=audio_file_name
        )

        # Asigna el archivo de audio a la instancia de Archivo
        return Archivo.objects.create(archivo=content, nombre=file.name[:-4])
