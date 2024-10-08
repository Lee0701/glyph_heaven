FROM python:3.9-bookworm

WORKDIR /usr/src/app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "glyph_heaven.wsgi:application", "-c", "gunicorn.conf.py"]
