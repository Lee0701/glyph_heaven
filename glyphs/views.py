from django.shortcuts import render, get_object_or_404
from .models import Glyph, Tag

# Create your views here.

def index(request):
    glyphs = Glyph.objects.all()
    return render(request, 'glyphs/index.html', {'glyphs': glyphs})

def detail(request, id):
    glyph = get_object_or_404(Glyph, id=id)
    return render(request, 'glyphs/detail.html', {'glyph': glyph})

def tag(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    glyphs = tag.glyph_set.all()
    return render(request, 'glyphs/tag.html', {'tag': tag, 'glyphs': glyphs})
