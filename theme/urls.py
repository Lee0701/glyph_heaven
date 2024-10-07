from django.urls import path
from django.conf.urls.static import static

from itertools import chain

urlpatterns = [
]

urlpatterns += chain.from_iterable([
    static('dist/', document_root='theme/dist/'),
])
