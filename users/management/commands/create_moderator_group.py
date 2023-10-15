from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        moderator_group = Group.objects.create(name='moderator_group')
        moderator_group.permissions.add(
            Permission.objects.get(codename='view_lesson'),
            Permission.objects.get(codename='change_lesson'),
            Permission.objects.get(codename='view_course'),
            Permission.objects.get(codename='change_course'),
        )
        moderator_group.save()
