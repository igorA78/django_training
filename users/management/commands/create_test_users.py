from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1 = User.objects.create(
            email='user1@mail.com'
        )
        user1.set_password('12345678')
        user1.save()

        user2 = User.objects.create(
            email='user2@mail.com'
        )
        user2.set_password('12345678')
        user2.save()
