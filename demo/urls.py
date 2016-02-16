from django.conf.urls import url
from . import views
urlpatterns = [url(r'^/$', views.index , name='semua_kelas'),
                        url(r'^create/$', views.create, name='create_kelas'),
                        url(r'^(?P<pk>\d+)/$', views.detail, name='kelas_detail'),
                        url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit_kelas'),
                        ]