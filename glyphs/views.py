from django.shortcuts import render, get_object_or_404, redirect
from .models import Glyph, Tag
from .forms import UploadForm

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

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, author=request.user, author_ip=request.META['REMOTE_ADDR'])
        if form.is_valid():
            glyph = form.save()
            return redirect('detail', id=glyph.id)
    else:
        form = UploadForm(author=request.user, author_ip=request.META['REMOTE_ADDR'])

    return render(request, 'glyphs/upload.html', {'form': form})
