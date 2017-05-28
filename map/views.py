from django.views import View
from django.http import HttpResponse


class MapIndex(View):
    def get(self, request):
        return HttpResponse('')
