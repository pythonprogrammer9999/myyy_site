
from django.urls import path, re_path
from django.http import HttpResponse



from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('delivery', delivery, name='delivery'),
    path('contacts', contacts, name='contacts'),
    re_path(r'^section/(?P<id>\d+)$', section, name='section'),
    re_path(r'^product/(?P<pk>\d+)$', ProductDetailView.as_view(), name='product'),
    path('search', search, name='search'),
]
