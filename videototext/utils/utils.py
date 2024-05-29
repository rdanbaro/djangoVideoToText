import configparser

from django.conf import settings


def read_config(endpoint=None):
    config = configparser.ConfigParser()
    config.read(settings.BASE_DIR / 'videototext/config.ini')

    # Lee los valores de las secciones
    #host = config.get('HOST', 'hostname')
    #port = config.getint('PORT', 'port_number')
    
    host = 'https://djangovideototext-production.up.railway.app/'
    port = '6187'
    
    api_url = config.get('URLS', endpoint if endpoint else 'transcription_app')

    if endpoint:
        return api_url

    return host, port, api_url
