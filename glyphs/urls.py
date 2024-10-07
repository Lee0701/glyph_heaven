from django.urls import path
from django.conf.urls.static import static
from glyph_heaven import settings
from . import views

from itertools import chain

urlpatterns = [
    path('', views.index, name='index'),
    path('id/<int:id>', views.glyph_detail, name='glyph_detail'),
    path('tag/<str:name>', views.tag_detail, name='tag_detail'),
    path('upload/', views.upload, name='upload'),
    path('id/<int:id>/edit/', views.edit_glyph, name='edit_glyph'),
    path('tag/<str:name>/edit/', views.edit_tag, name='edit_tag'),
    path('id/<int:id>/add_tag/<str:name>', views.add_tag, name='add_tag'),
    path('id/<int:id>/remove_tag/<str:name>', views.remove_tag, name='remove_tag'),
]

urlpatterns += chain.from_iterable([
    static('image/', document_root=settings.UPLOAD_DIR),
])
