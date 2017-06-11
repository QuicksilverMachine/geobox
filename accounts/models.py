import os
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_cleanup.signals import cleanup_post_delete
from webapp.settings import STATIC_URL


class UserManager(BaseUserManager):
    def create_user(self, username, full_name, email, password=None):
        user = self.model(
            username=username,
            full_name=full_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, full_name, email, password):
        user = self.create_user(
            username=username,
            full_name=full_name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


def profile_picture_upload_path(instance, filename):
    return os.path.join(
        "accounts/profile_pictures/%s/" % instance.username, filename)


class User(AbstractUser):
    is_active = models.BooleanField(_("Is active"), default=True)
    is_admin = models.BooleanField(_("Is admin"), default=False)
    full_name = models.CharField(_("Full name"), max_length=100)
    profile_picture = models.FileField(_("Profile picture"),
                                       upload_to=profile_picture_upload_path,
                                       blank=True,
                                       null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return os.path.join(STATIC_URL, 'accounts/img/user-icon.png')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account_profile', kwargs={'username': self.username})

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# Receive the post_save signal and add id to username
# This solves the problem of user impersonation by using
# visually similar unicode characters
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        instance.username = "%s_%s" % (instance.username, instance.id)
        instance.save()


# Receive the pre_delete signal and delete the files
# associated with the model instance.
@receiver(post_delete, sender=User)
def user_delete(sender, instance, **kwargs):
    cleanup_post_delete.send(sender)
