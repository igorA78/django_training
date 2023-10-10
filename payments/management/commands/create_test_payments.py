from datetime import date, timedelta

from django.core.management import BaseCommand

from education.models import Lesson, Course
from payments.models import Payment
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()
        lesson = Lesson.objects.first()
        course = Course.objects.first()
        today_date = date.today()
        yesterday_date = date.today() - timedelta(days=1)

        Payment.objects.create(
            user=user,
            payment_date=yesterday_date,
            course=course,
            amount=15000,
            payment_type='card',
        )

        Payment.objects.create(
            user=user,
            payment_date=today_date,
            course=course,
            amount=20000,
            payment_type='cash',
        )

        Payment.objects.create(
            user=user,
            payment_date=yesterday_date,
            lesson=lesson,
            amount=2500,
            payment_type='cash',
        )

        Payment.objects.create(
            user=user,
            payment_date=today_date,
            lesson=lesson,
            amount=1500,
            payment_type='card',
        )

