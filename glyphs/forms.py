from django import forms
from .models import Glyph, Tag
from .functions import normalize

textarea_attrs = {'class': 'textarea', 'rows': 8}

class UploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author, self.author_name, self.author_ip = kwargs.pop('author')

        super(UploadForm, self).__init__(*args, **kwargs)

    image = forms.ImageField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs), required=False)
    tags = forms.CharField(required=True)

    def save(self, commit=True):
        glyph = super(UploadForm, self).save(commit=False)
        glyph.author = self.author
        glyph.author_name = self.author_name
        glyph.author_ip = self.author_ip
        glyph.save(commit)

        tags = normalize(self.cleaned_data['tags'].strip()).split()
        for tagname in tags:
            tag, _ = Tag.objects.get_or_create(
                name=tagname,
                defaults={'author': self.author, 'author_name': self.author_name, 'author_ip': self.author_ip}
            )
            glyph.tags.add(tag)
        return glyph

    class Meta:
        model = Glyph
        fields = ['image', 'description', 'tags']

class SimpleUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author, self.author_name, self.author_ip = kwargs.pop('author')
        self.tag = kwargs.pop('tag')

        super(SimpleUploadForm, self).__init__(*args, **kwargs)

    image = forms.ImageField(required=True)

    def save(self, commit=True):
        glyph = super(SimpleUploadForm, self).save(commit=False)
        glyph.author = self.author
        glyph.author_name = self.author_name
        glyph.author_ip = self.author_ip
        glyph.save(commit)

        glyph.tags.add(self.tag)

        return glyph

    class Meta:
        model = Glyph
        fields = ['image']

class EditGlyphForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.glyph = kwargs.pop('glyph')
        self.author, self.author_name, self.author_ip = kwargs.pop('author')

        super(EditGlyphForm, self).__init__(*args, **kwargs)

        self.initial['description'] = self.glyph.description
        self.initial['tags'] = ' '.join(self.glyph.tags.values_list('name', flat=True))

    description = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs), required=False)
    tags = forms.CharField(required=True)

    def save(self, commit=True):
        self.glyph.description = self.cleaned_data['description']
        self.glyph.save(update_fields=['description'])

        self.glyph.tags.clear()
        tags = normalize(self.cleaned_data['tags'].strip()).split()
        for tagname in tags:
            tag, _ = Tag.objects.get_or_create(
                name=tagname,
                defaults={'author': self.author, 'author_name': self.author_name, 'author_ip': self.author_ip}
            )
            self.glyph.tags.add(tag)

        return self.glyph

class EditTagForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.tag = kwargs.pop('tag')
        self.author, self.author_name, self.author_ip = kwargs.pop('author')

        super(EditTagForm, self).__init__(*args, **kwargs)

        self.initial['kage'] = self.tag.kage
        self.initial['description'] = self.tag.description
        self.initial['tags'] = ' '.join(self.tag.tags.values_list('name', flat=True))
    
    kage = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs), required=False)
    tags = forms.CharField(required=True)

    def save(self, commit=True):
        self.tag.kage = self.cleaned_data['kage']
        self.tag.description = self.cleaned_data['description']
        self.tag.save(update_fields=['kage', 'description'])

        self.tag.tags.clear()
        tags = normalize(self.cleaned_data['tags'].strip()).split()
        for tagname in tags:
            tag, _ = Tag.objects.get_or_create(
                name=tagname,
                defaults={'author': self.author, 'author_name': self.author_name, 'author_ip': self.author_ip}
            )
            self.tag.tags.add(tag)

        return self.tag
