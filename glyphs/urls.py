from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('id/<int:id>/', views.glyph_detail, name='glyph_detail'),
    path('tag/<str:name>/', views.tag_detail, name='tag_detail'),
    path('id/<int:id>/edit/', views.edit_glyph, name='edit_glyph'),
    path('tag/<str:name>/edit/', views.edit_tag, name='edit_tag'),

    path('upload/', views.upload, name='upload'),
    path('tag/<str:name>/upload/', views.simple_upload, name='simple_upload'),

    path('id/<int:id>/add_tag/<str:name>/', views.add_glyph_tag, name='add_glyph_tag'),
    path('id/<int:id>/remove_tag/<str:name>/', views.remove_glyph_tag, name='remove_glyph_tag'),
    path('tag/<str:to_name>/add_tag/<str:name>/', views.add_tag_tag, name='add_tag_tag'),
    path('tag/<str:to_name>/remove_tag/<str:name>/', views.remove_tag_tag, name='remove_tag_tag'),

    path('search/', views.search, name='search'),
]
