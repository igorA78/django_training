from rest_framework import test, status

from education.models import Course
from subscriptions.models import Subscription
from users.models import User


class SubscriptionAPITestCase(test.APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(email='user1@mail.com', password='1234')
        self.user2 = User.objects.create(email='user2@mail.com', password='1234')
        self.course = Course.objects.create(title='test course', description='test', owner=self.user1)
        self.client = test.APIClient()

    def test_create_subscription(self):
        data = {
            'user': self.user1.pk,
            'course': self.course.pk
        }
        url = '/subscriptions/create/'

        # 1. Неавторизованный пользователь не может создать подписку
        response = self.client.post(url, data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. Авторизованный пользователь может создать подписку
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 1, 'user': self.user1.pk, 'course': self.course.pk}
        )

    def test_destroy_subscription(self):
        subscription = Subscription.objects.create(
            user=self.user1,
            course=self.course
        )
        url = f'/subscriptions/delete/{subscription.pk}/'

        # 1. Неавторизованный пользователь не может удалить подписку
        response = self.client.delete(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


        # 2. Авторизованный пользователь может удалить подписку
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEquals(
            Subscription.objects.all().count(),
            0
        )



    def test_display_subscription(self):
        url = f'/courses/{self.course.pk}/'
        self.client.force_authenticate(user=self.user1)

        # 1. Таблица подписок пустая, отметка о подписке в курсе - False
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': self.course.pk, 'lessons_count': 0, 'lessons': [], 'is_subscribed': False,
             'title': 'test course', 'description': 'test', 'preview': None, 'owner': self.user1.pk}
        )

        # 2. Создали подписку у user1, отметка о подписке в курсе пользователя user1 - True
        subscription = Subscription.objects.create(
            user=self.user1,
            course=self.course
        )
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': self.course.pk, 'lessons_count': 0, 'lessons': [], 'is_subscribed': True,
             'title': 'test course', 'description': 'test', 'preview': None, 'owner': self.user1.pk}
        )

        # 3. Удалили подписку у user1, отметка о подписке в курсе пользователя user1 - False
        subscription.delete()
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': self.course.pk, 'lessons_count': 0, 'lessons': [], 'is_subscribed': False,
             'title': 'test course', 'description': 'test', 'preview': None, 'owner': self.user1.pk}
        )

        # 4. Создали подписку у user2, отметка о подписке в курсе пользователя user1 - False
        subscription = Subscription.objects.create(
            user=self.user2,
            course=self.course
        )
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': self.course.pk, 'lessons_count': 0, 'lessons': [], 'is_subscribed': False,
             'title': 'test course', 'description': 'test', 'preview': None, 'owner': self.user1.pk}
        )
