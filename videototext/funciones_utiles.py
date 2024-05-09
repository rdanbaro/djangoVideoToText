import mimetypes

def es_video(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('video/')

def es_audio(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('audio/')