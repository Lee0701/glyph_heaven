
from glyph_heaven import settings

import os
import hashlib
from functools import partial

def image_url(url):
    filename = os.path.split(url)[1]
    prefix = filename[:2]
    return f'/glyphs/image/{prefix}/{filename}'

def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()


def upload_to(instance, filename):
    """
    :type instance: dolphin.models.File
    """
    instance.image.open()
    filename, ext = os.path.splitext(filename)
    filename = hash_file(instance.image)
    prefix = filename[:2]
    path = settings.UPLOAD_DIR

    file_path = f'{path}/{prefix}/{filename}{ext}'
    return file_path

def get_author_info(request):
    author = request.user if request.user.is_authenticated else None
    author_name = author.username if author else ''
    author_ip = request.META['REMOTE_ADDR']
    return author, author_name, author_ip

def get_author_name(glyph_or_tag):
    if glyph_or_tag.author:
        return glyph_or_tag.author.username
    elif glyph_or_tag.author_name:
        return glyph_or_tag.author_name
    else:
        return glyph_or_tag.author_ip
