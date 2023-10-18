from django.contrib.auth.models import Group, Permission
from rest_framework import test, status

from education.models import Lesson
from users.models import User


class LessonsTestCase(test.APITestCase):
    def setUp(self) -> None:
        self.client = test.APIClient()
        self.create_users()
        self.create_moderator()

    def create_users(self):
        self.user1 = User.objects.create(email='user1@mail.com', password='1234')

        self.user2 = User.objects.create(email='user2@mail.com', password='1234')

    def create_moderator(self):
        moderator_group = Group.objects.create(name='moderator_group')

        moderator_group.permissions.add(
            Permission.objects.get(codename='view_lesson'),
            Permission.objects.get(codename='change_lesson'),
            Permission.objects.get(codename='view_course'),
            Permission.objects.get(codename='change_course'),
        )
        moderator_group.save()

        self.moderator = User.objects.create(email='moderator@mail.com', password='1234')
        self.moderator.groups.add(moderator_group)
        self.moderator.save()

    def test_create_lesson(self):
        data = {
            'title': 'test lesson 1',
            'description': 'test description'
        }
        url = '/lessons/create/'

        # 1. Не авторизованный пользователь не может создать урок
        response = self.client.post(url, data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. Модератор не может создать урок
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_list_lessons(self):
        lesson = Lesson.objects.create(
            title='test lesson 1',
            description='test description',
            owner=self.user1
        )
        url = '/lessons/'

        # 1. Нет доступа у неавторизованного пользователя
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. У пользователя user1 есть его урок, и урок отображается
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': lesson.pk, 'title': 'test lesson 1', 'description': 'test description', 'preview': None,
                 'video_url': None, 'course': None, 'owner': self.user1.pk}]}
        )

        # 3. У пользователя user2 нет уроков, список пуст
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'count': 0, 'next': None, 'previous': None, 'results': []}
        )

        # 4. У модератора есть доступ, созданный урок отображается
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': lesson.pk, 'title': 'test lesson 1', 'description': 'test description', 'preview': None,
                 'video_url': None, 'course': None, 'owner': self.user1.pk}]}
        )

    def test_retrieve_lessons(self):
        lesson = Lesson.objects.create(
            title='test lesson 1',
            description='test description',
            owner=self.user1
        )
        url = f'/lessons/{lesson.pk}/'

        # 1. Нет доступа у неавторизованного пользователя
        response = self.client.get(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. У владельца есть доступ
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': lesson.pk, 'title': 'test lesson 1', 'description': 'test description', 'preview': None,
             'video_url': None, 'course': None, 'owner': self.user1.pk}
        )

        # 3. У авторизованного пользователя не владельца нет доступа
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # 4. У модератора есть доступ, данные корректно отображаются
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': lesson.pk, 'title': 'test lesson 1', 'description': 'test description', 'preview': None,
             'video_url': None, 'course': None, 'owner': self.user1.pk}
        )

    def test_update_lessons(self):
        lesson = Lesson.objects.create(
            title='test lesson 1',
            description='test description',
            owner=self.user1
        )
        data_user = {
            'title': 'test lesson 1 user'
        }
        data_moderator = {
            'title': 'test lesson 1 moderator'
        }
        url = f'/lessons/update/{lesson.pk}/'

        # 1. Нет доступа у неавторизованного пользователя
        response = self.client.put(url, data=data_user)
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. У владельца есть доступ, данные обновляются
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(url, data=data_user)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': lesson.pk, 'title': 'test lesson 1 user', 'description': 'test description', 'preview': None,
             'video_url': None, 'course': None, 'owner': self.user1.pk}
        )

        # 3. У авторизованного пользователя не владельца нет доступа
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data=data_user)

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # 4. У модератора есть доступ, данные обновляются
        self.client.force_authenticate(user=self.moderator)
        response = self.client.put(url, data=data_moderator)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'id': lesson.pk, 'title': 'test lesson 1 moderator', 'description': 'test description', 'preview': None,
             'video_url': None, 'course': None, 'owner': self.user1.pk}
        )

    def test_destroy_lessons(self):
        lesson = Lesson.objects.create(
            title='test lesson 1',
            description='test description',
            owner=self.user1
        )
        url = f'/lessons/delete/{lesson.pk}/'

        # 1. Нет доступа у неавторизованного пользователя
        response = self.client.delete(url)
        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # 2. У авторизованного пользователя не владельца нет доступа
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # 3. У модератора нет доступа
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # 4. У владельца есть доступ, данные удаляются
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        response = self.client.get('/lessons/')
        self.assertEquals(
            response.json(),
            {'count': 0, 'next': None, 'previous': None, 'results': []}
        )
