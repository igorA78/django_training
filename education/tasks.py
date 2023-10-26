from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Course
from subscriptions.models import Subscription


@shared_task
def send_mail_for_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in subscriptions:
        send_mail(subject=f"Обновленные материалы курса{course.title}",
                  message=f"у вас есть несколько обновлений в {course.title}, проверьте",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[subscription.user.email],
                  fail_silently=True
                  )
