from django.views import generic
from map.models import Map


class MapIndexView(generic.ListView):
    template_name = 'map/index.html'
    context_object_name = 'maps'

    def get_queryset(self):
        media = Map.objects.all()
        return media


class MapDetailView(generic.DetailView):
    model = Map
    template_name = 'map/map.html'
    context_object_name = 'map'
