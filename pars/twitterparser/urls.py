from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.begin),
    url(r'^how_to/$', views.how_to),
    url(r'^search/$', views.search),
    url(r'^result/$', views.result),
    url(r'^result/download/$', views.download),
]
