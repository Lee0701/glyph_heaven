from django.shortcuts import render, redirect, get_object_or_404
from .models import Glyph, Tag
from . import forms

# Create your views here.

def index(request):
    glyphs = Glyph.objects.all()
    return render(request, 'glyphs/index.html', {'glyphs': glyphs})

def glyph_detail(request, id):
    glyph = get_object_or_404(Glyph, id=id)
    return render(request, 'glyphs/glyph_detail.html', {'glyph': glyph})

def tag_detail(request, name):
    tag = get_object_or_404(Tag, name=name)
    glyphs = tag.glyph_set.all()
    return render(request, 'glyphs/tag_detail.html', {'tag': tag, 'glyphs': glyphs})

def upload(request):
    author = request.user
    author_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        form = forms.UploadForm(request.POST, request.FILES, author=author, author_ip=author_ip)
        if form.is_valid():
            glyph = form.save()
            return redirect('glyph_detail', id=glyph.id)
    else:
        form = forms.UploadForm(author=author, author_ip=author_ip)

    return render(request, 'glyphs/upload.html', {'form': form})

def edit_glyph(request, id):
    glyph = get_object_or_404(Glyph, id=id)
    if request.method == 'POST':
        form = forms.EditGlyphForm(request.POST, request.FILES, glyph=glyph)
        if form.is_valid():
            glyph = form.save()
            return redirect('glyph_detail', id=glyph.id)
    else:
        form = forms.EditGlyphForm(glyph=glyph)

    return render(request, 'glyphs/edit_glyph.html', {'form': form, 'glyph': glyph})

def edit_tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    if request.method == 'POST':
        form = forms.EditTagForm(request.POST, tag=tag)
        if form.is_valid():
            tag = form.save()
            return redirect('tag_detail', tag=tag.name)
    else:
        form = forms.EditTagForm(tag=tag)

    return render(request, 'glyphs/edit_tag.html', {'form': form, 'tag': tag})

def add_tag(request, id, name):
    glyph = get_object_or_404(Glyph, id=id)
    tag, created = Tag.objects.get_or_create(name=name)
    if created:
        tag.author = request.user
        tag.author_name = request.user.username if request.user.is_authenticated else ''
        tag.author_ip = request.META['REMOTE_ADDR']
        tag.save()
    glyph.tags.add(tag)
    return redirect('glyph_detail', id=glyph.id)

def remove_tag(request, id, name):
    glyph = get_object_or_404(Glyph, id=id)
    tag = get_object_or_404(Tag, name=name)
    if request.user.is_authenticated or glyph.author_ip == request.META['REMOTE_ADDR']:
        glyph.tags.remove(tag)
    return redirect('glyph_detail', id=glyph.id)
