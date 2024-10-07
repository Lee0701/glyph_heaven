from django.db import models
from glyph_heaven import settings
from users.models import User

import os
import hashlib
from functools import partial

# Create your models here.

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

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('self', symmetrical=False, blank=True)

    def href(self):
        return f'/glyphs/tag/{self.name}'

class Glyph(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_ip = models.GenericIPAddressField()
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    kage = models.TextField(blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def image_url(self):
        url = self.image.url
        filename = os.path.split(url)[1]
        prefix = filename[:2]
        return f'/glyphs/image/{prefix}/{filename}'
    
    def detail_url(self):
        return f'/glyphs/id/{self.id}'

    class Meta:
        ordering = ['-created_at']
