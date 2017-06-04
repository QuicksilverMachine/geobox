from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Map(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"))
    created = models.DateTimeField(_("Created"), default=now)
    # user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
