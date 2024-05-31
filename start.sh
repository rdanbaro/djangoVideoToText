#!/bin/bash
python manage.py collectstatic --noinput
gunicorn --timeout 120 djangoVideoToText.wsgi
