from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class Map(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"))
    created = models.DateTimeField(_("Created"), default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
