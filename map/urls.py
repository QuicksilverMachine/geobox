from django.conf.urls import url

from map import views

urlpatterns = [
    url(r'^$', views.MapIndexView.as_view(), name='index'),
    url(r'^(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$',
        views.MapDetailView.as_view(), name='detail'),
    url(r'^create/$', views.create_map, name='create'),
    url(r'^update/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$',
        views.update_map,
        name='update'),
    url(r'^delete/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$',
        views.delete_map,
        name='delete'),
    url(r'^waypoints/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$', views.update_map_wp,
        name='waypoints'),
    url(r'^get_users/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}'
        r'-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$', views.update_user_sessions,
        name='get_users'),
    url(r'^add_users$', views.add_user_sessions, name='add_users'),
]
