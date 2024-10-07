from django.urls import path
from django.conf.urls.static import static
from glyph_heaven import settings
from . import views

from itertools import chain

urlpatterns = [
    path('', views.index, name='index'),
    path('id/<int:id>', views.glyph_detail, name='glyph_detail'),
    path('tag/<str:tag>', views.tag_detail, name='tag_detail'),
    path('upload/', views.upload, name='upload'),
]

urlpatterns += chain.from_iterable([
    static('image/', document_root=settings.UPLOAD_DIR),
])
