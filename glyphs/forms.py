from django import forms
from .models import Glyph, Tag

class UploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        self.author_name = self.author.username
        self.author_ip = kwargs.pop('author_ip')
        super(UploadForm, self).__init__(*args, **kwargs)

    image = forms.FileField(required=True)
    kage = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False)
    tags = forms.CharField(required=True)

    def save(self, commit=True):
        glyph = super(UploadForm, self).save(commit=False)
        glyph.author = self.author
        glyph.author_name = self.author_name
        glyph.author_ip = self.author_ip
        glyph.save(commit)

        tags = self.cleaned_data['tags'].split()
        for tagname in tags:
            tag, created = Tag.objects.get_or_create(name=tagname)
            if created:
                tag.author = self.author
                tag.author_name = self.author_name
                tag.author_ip = self.author_ip
                tag.save(commit)
            glyph.tags.add(tag)
        return glyph

    class Meta:
        model = Glyph
        fields = ['image', 'kage', 'description', 'tags']

class EditGlyphForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.glyph = kwargs.pop('glyph')
        super(EditGlyphForm, self).__init__(*args, **kwargs)
        self.initial['description'] = self.glyph.description

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False)

    def save(self, commit=True):
        self.glyph.description = self.cleaned_data['description']
        self.glyph.save(update_fields=['description'])
        return self.glyph

class EditTagForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.tag = kwargs.pop('tag')
        super(EditTagForm, self).__init__(*args, **kwargs)
        self.initial['kage'] = self.tag.kage
        self.initial['description'] = self.tag.description
    
    kage = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False)

    def save(self, commit=True):
        self.tag.kage = self.cleaned_data['kage']
        self.tag.description = self.cleaned_data['description']
        self.tag.save(update_fields=['kage', 'description'])
        return self.tag
