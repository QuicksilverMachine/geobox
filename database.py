#!/usr/bin/python3
import os
import shutil
import uuid

import django
from faker import Factory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
django.setup()

fake = Factory.create()


def delete_users():
    from accounts.models import User
    User.objects.all().delete()
    dir_path = "media/accounts/profile_pictures/"
    user_list = next(os.walk(dir_path))[1]
    for user in user_list:
        shutil.rmtree(dir_path + user)


def delete_maps():
    from map.models import Map
    Map.objects.all().delete()


def reset_users():
    print("Resetting users...")
    from accounts.models import User

    delete_users()

    User.objects.create_superuser(
        username='admin',
        full_name='Administrator',
        email='quicksilver.machine@gmail.com',
        password='admin')
    for i in range(1, 11):
        user = User.objects.create_user(
            username=fake.user_name(),
            full_name=fake.name(),
            email="user%s@example.com" % i,
            password="password")
        user.save()


def reset_maps():
    print("Resetting maps...")
    from map.models import Map

    delete_maps()

    for i in range(1, 11):
        new_map = Map()
        new_map.id = uuid.uuid4()
        new_map.title = 'title-{}'.format(i)
        new_map.description = 'description-{}'.format(i)
        new_map.user_id = i
        new_map.save()


def reset_db():
    reset_users()
    reset_maps()
    print("Done.")


if __name__ == "__main__":
    reset_db()
