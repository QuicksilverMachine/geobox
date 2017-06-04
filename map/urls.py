from django.conf.urls import url

from map import views

urlpatterns = [
    url(r'^$', views.MapIndexView.as_view(), name='index'),
]
