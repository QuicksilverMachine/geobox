from django.conf.urls import url

from map import views

urlpatterns = [
    url(r'^$', views.MapIndex.as_view(), name='index'),
]
