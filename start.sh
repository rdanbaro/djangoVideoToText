#!/bin/bash
sudo apt install ffmpeg
python manage.py collectstatic --noinput
gunicorn --timeout 120 djangoVideoToText.wsgi
