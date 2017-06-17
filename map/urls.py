from django.conf.urls import url

from map import views

urlpatterns = [
    url(r'^$', views.MapIndexView.as_view(), name='index'),
    url(r'^(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$',
        views.MapDetailView.as_view(), name='detail'),
]
