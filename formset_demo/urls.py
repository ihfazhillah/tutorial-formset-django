from django.conf.urls import include, url

urlpatterns = [url(r'^demo/', include('demo.urls'))]
