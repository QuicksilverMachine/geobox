from django.views import View
from django.http import HttpResponse

from django.views import generic
from map.models import Map


class MapIndexView(generic.ListView):
    template_name = 'map/index.html'
    context_object_name = 'maps'

    def get_queryset(self):
        media = Map.objects.all()
        return media
