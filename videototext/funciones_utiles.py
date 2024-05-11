import mimetypes
from django.conf import settings
import moviepy.editor as mp

def es_video(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('video/')

def es_audio(archivo):
    tipo_mime = mimetypes.guess_type(archivo.name)[0]
    return tipo_mime.startswith('audio/')

def conversion(url):
    
    print('url:  ', url)
    clip = mp.VideoFileClip(url)
    #print('clip_var', clip)
    clip.audio.write_audiofile(url[:-4] + '.mp3')
    