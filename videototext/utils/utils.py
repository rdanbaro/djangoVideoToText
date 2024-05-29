import configparser

from django.conf import settings


def read_config(endpoint=None):
    config = configparser.ConfigParser()
    config.read(settings.BASE_DIR / 'videototext/config.ini')

    # Si estás usando un URL completo, no necesitas especificar el puerto por separado
    host = 'https://djangovideototext-production.up.railway.app'
    api_url = config.get('URLS', endpoint if endpoint else 'transcription_app')

    if endpoint:
        return f'{host}/{api_url}'

    return host, api_url

