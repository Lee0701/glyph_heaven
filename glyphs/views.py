from django.shortcuts import render, redirect, get_object_or_404
from .models import Glyph, Tag
from .functions import get_author_info
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

    form = forms.SimpleUploadForm(author=get_author_info(request), tag=tag)

    return render(request, 'glyphs/tag_detail.html', {'form': form, 'tag': tag, 'glyphs': glyphs})

def upload(request):
    if request.method == 'POST':
        form = forms.UploadForm(request.POST, request.FILES, author=get_author_info(request))
        if form.is_valid():
            glyph = form.save()
            return redirect('glyph_detail', id=glyph.id)
    else:
        form = forms.UploadForm(author=get_author_info(request))

    return render(request, 'glyphs/upload.html', {'form': form})

def simple_upload(request, name):
    tag = get_object_or_404(Tag, name=name)
    if request.method == 'POST':
        form = forms.SimpleUploadForm(request.POST, request.FILES, author=get_author_info(request), tag=tag)
        if form.is_valid():
            glyph = form.save()
            return redirect('glyph_detail', id=glyph.id)
    else:
        form = forms.SimpleUploadForm(author=get_author_info(request), tag=tag)

    return render(request, 'glyphs/upload.html', {'form': form})

def edit_glyph(request, id):
    glyph = get_object_or_404(Glyph, id=id)
    if request.method == 'POST':
        form = forms.EditGlyphForm(request.POST, request.FILES, glyph=glyph, author=get_author_info(request))
        if form.is_valid():
            glyph = form.save()
            return redirect('glyph_detail', id=glyph.id)
    else:
        form = forms.EditGlyphForm(glyph=glyph, author=get_author_info(request))

    return render(request, 'glyphs/edit_glyph.html', {'form': form, 'glyph': glyph})

def edit_tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    if request.method == 'POST':
        form = forms.EditTagForm(request.POST, tag=tag, author=get_author_info(request))
        if form.is_valid():
            tag = form.save()
            return redirect('tag_detail', name=tag.name)
    else:
        form = forms.EditTagForm(tag=tag, author=get_author_info(request))

    return render(request, 'glyphs/edit_tag.html', {'form': form, 'tag': tag})

def add_glyph_tag(request, id, name):
    author = request.user if request.user.is_authenticated else None
    author_name = request.user.username if request.user.is_authenticated else ''
    author_ip = request.META['REMOTE_ADDR']
    glyph = get_object_or_404(Glyph, id=id)
    tag, _ = Tag.objects.get_or_create(
        name=name,
        defaults={'author': author, 'author_name': author_name, 'author_ip': author_ip}
    )
    glyph.tags.add(tag)
    return redirect('glyph_detail', id=glyph.id)

def remove_glyph_tag(request, id, name):
    glyph = get_object_or_404(Glyph, id=id)
    tag = get_object_or_404(Tag, name=name)
    if request.user.is_authenticated or glyph.author_ip == request.META['REMOTE_ADDR']:
        glyph.tags.remove(tag)
    return redirect('glyph_detail', id=glyph.id)

def add_tag_tag(request, to_name, name):
    author = request.user if request.user.is_authenticated else None
    author_name = request.user.username if request.user.is_authenticated else ''
    author_ip = request.META['REMOTE_ADDR']
    tag = get_object_or_404(Tag, name=to_name)
    tag, _ = Tag.objects.get_or_create(
        name=name,
        defaults={'author': author, 'author_name': author_name, 'author_ip': author_ip}
    )
    tag.tags.add(t)
    return redirect('tag_detail', name=to_name)

def remove_tag_tag(request, to_name, name):
    tag = get_object_or_404(Tag, name=to_name)
    t = get_object_or_404(Tag, name=name)
    if request.user.is_authenticated or tag.author_ip == request.META['REMOTE_ADDR']:
        tag.tags.remove(t)
    return redirect('tag_detail', name=to_name)
