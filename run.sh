#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn glyph_heaven.wsgi:application -c gunicorn.conf.py
