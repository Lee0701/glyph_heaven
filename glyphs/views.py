from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from annoying.functions import get_object_or_None
from .models import Glyph, Tag
from .functions import get_author_info
from . import forms

# Create your views here.

def index(request, page=1):
    glyphs = Glyph.objects.all()
    paginator = Paginator(glyphs, 20)
    glyphs = paginator.get_page(page)
    return render(request, 'glyphs/index.html', {'glyphs': glyphs})

def glyph_detail(request, id):
    glyph = get_object_or_None(Glyph, id=id)
    if glyph is None:
        message = f'No glyph found with id {id}.'
        return render(request, 'glyphs/404.html', {'message': message}, status=404)
    return render(request, 'glyphs/glyph_detail.html', {'glyph': glyph})

def tag_detail(request, name):
    tag = get_object_or_None(Tag, name=name)
    if tag is None:
        message = f'No tag found with name {name}.'
        return render(request, 'glyphs/404.html', {'message': message}, status=404)
    glyphs = tag.glyph_set.all()

    form = forms.SimpleUploadForm(author=get_author_info(request), tag=tag)

    return render(request, 'glyphs/tag_detail.html', {'form': form, 'tag': tag, 'glyphs': glyphs})

def search(request):
    query = request.GET.get('query', '')
    if query == '':
        return redirect('index')
    return redirect('tag_detail', name=query)

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
        form = forms.EditGlyphForm(request.POST, glyph=glyph, author=get_author_info(request))
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
    author, author_name, author_ip = get_author_info(request)
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
    author, author_name, author_ip = get_author_info(request)
    tag = get_object_or_404(Tag, name=to_name)
    t, _ = Tag.objects.get_or_create(
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
