from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class Map(models.Model):
    id = models.TextField(primary_key=True)
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"))
    created = models.DateTimeField(_("Created"), default=now)
    editing = models.BooleanField(_("Editing"), default=True)
    private = models.BooleanField(_("Private"), default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Waypoint(models.Model):
    id = models.IntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    @staticmethod
    def packed(waypoint_map_id):
        waypoints = Waypoint.objects.filter(map=waypoint_map_id)
        packed_waypoints = ""
        for waypoint in waypoints:
            packed_waypoints = (
                packed_waypoints +
                "|" +
                str(waypoint.latitude) +
                "/" +
                str(waypoint.longitude)
            )
        return packed_waypoints
