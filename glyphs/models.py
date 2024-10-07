from django.db import models
from users.models import User

from .image_funcs import image_url, upload_to

# Create your models here.

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
        return image_url(url)

    def detail_url(self):
        return f'/glyphs/id/{self.id}'

    class Meta:
        ordering = ['-created_at']
