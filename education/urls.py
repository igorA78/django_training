from django.urls import path
from rest_framework import routers

from education.apps import EducationConfig
from education.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = EducationConfig.name


router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')


urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lessons/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls


