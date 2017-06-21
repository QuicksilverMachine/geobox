import datetime
import uuid

import json
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt

from map.models import Map, Waypoint, UserSession, User


class MapIndexView(generic.ListView):
    template_name = 'map/index.html'
    context_object_name = 'maps'

    def get_queryset(self):
        maps = Map.objects.all()
        return maps


class MapDetailView(generic.DetailView):
    model = Map
    template_name = 'map/map.html'
    context_object_name = 'map'

    def get_object(self, queryset=None):

        queried_map = super(MapDetailView, self).get_object()
        if self.request.user != queried_map.user and queried_map.private:
            raise Http404
        return queried_map

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['map'].user != self.request.user:
            context['map'].editing = False
        context['waypoints'] = Waypoint.packed(context['map'].id)
        return context


def create_map(request):
    if not request.user.is_authenticated.value:
        return HttpResponse(status=403)

    new_map_id = uuid.uuid4()
    user_maps_count = request.user.map_set.count()
    new_map = Map(
        id=new_map_id,
        user=request.user,
        title="Map-{}".format(user_maps_count + 1),
    )
    new_map.save()
    return redirect('/map/{}'.format(new_map_id))


def delete_map(request, pk):
    if not request.user.is_authenticated.value:
        return HttpResponse(status=404)

    map_to_delete = Map.objects.get(id=pk)

    if request.user != map_to_delete.user:
        return HttpResponse(status=404)

    map_to_delete.delete()
    return redirect('/map/')


def update_map(request, pk):
    if not request.user.is_authenticated.value:
        return HttpResponse(status=404)

    map_to_update = Map.objects.get(id=pk)

    if request.user != map_to_update.user:
        return HttpResponse(status=404)

    map_to_update.title = request.POST.get('title', map_to_update.title)
    map_to_update.description = request.POST.get('description',
                                                 map_to_update.description)
    map_to_update.editing = True if request.POST.get('editing') else False
    map_to_update.private = True if request.POST.get('private') else False
    map_to_update.save()

    packed_waypoints = request.POST.get('waypoints', "")
    new_waypoints = [wp for wp in packed_waypoints.split('|') if wp]

    try:
        # Delete old waypoints
        old_waypoints = Waypoint.objects.filter(map__user=request.user)
        old_waypoints.delete()
    except Waypoint.DoesNotExist:
        pass

    for wp in new_waypoints:
        lat_lng = wp.split('/')
        waypoint = Waypoint(
            latitude=lat_lng[0],
            longitude=lat_lng[1],
            map=map_to_update
        )
        waypoint.save()

    return redirect('/map/{}'.format(pk))


def update_map_wp(request, pk):
    map_object = Map.objects.get(id=pk)

    if map_object.private and not map_object.user == request.user:
        return HttpResponse(status=404)

    return HttpResponse(Waypoint.packed(map_object.id))


@csrf_exempt
def add_user_sessions(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    pk = body['pk']
    latitude = body['latitude']
    longitude = body['longitude']

    map_object = Map.objects.get(id=pk)

    if map_object.private and not map_object.user == request.user:
        return HttpResponse(status=404)

    if not request.user.is_authenticated:
        user = User(
            full_name="Anonymous User"
        )
        user.save()
    else:
        user = request.user

    user_session = UserSession(
        user=user,
        map=map_object,
        timestamp=datetime.datetime.utcnow(),
        latitude=latitude,
        longitude=longitude
    )
    user_session.save()
    return HttpResponse(status=200)


def update_user_sessions(request, pk):
    user_sessions = (
        UserSession.objects
        .filter(map__id=pk)
        .filter(
            timestamp__gt=(
                datetime.datetime.now() - datetime.timedelta(seconds=20)
            ))).all()

    users = []
    usernames = []
    for session in user_sessions:
        if session.user.full_name not in usernames:
            usernames.append(session.user.full_name)
            users.append({
                "full_name": session.user.full_name,
                "latitude": session.latitude,
                "longitude": session.longitude
            })
    return JsonResponse({
        'users': users
    })
