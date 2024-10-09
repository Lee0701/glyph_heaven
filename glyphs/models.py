from django.db import models
from users.models import User

from .functions import image_url, upload_to, get_author_name

from pycmarkgfm import gfm_to_html

class Tag(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_ip = models.GenericIPAddressField()
    name = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    kage = models.TextField(blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('self', symmetrical=False, blank=True)

    def href(self):
        return f'/glyphs/tag/{self.name}'

    def rev_tags(self):
        return Tag.objects.filter(tags=self)
    
    def author_displayname(self):
        return get_author_name(self)

    def description_html(self):
        return gfm_to_html(self.description)

    class Meta:
        ordering = ['name']

class Glyph(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_ip = models.GenericIPAddressField()
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def image_url(self):
        url = self.image.url
        return image_url(url)

    def detail_url(self):
        return f'/glyphs/id/{self.id}'

    def author_displayname(self):
        return get_author_name(self)

    def description_html(self):
        return gfm_to_html(self.description)

    def tag_list(self):
        return ' '.join(self.tags.values_list('name', flat=True))

    class Meta:
        ordering = ['-created_at']
