from rest_framework import viewsets, generics

from education.models import Course, Lesson
from education.permissions import EducationItemAccess
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [EducationItemAccess]

    def get_queryset(self):
        queryset = Course.objects.all()
        if not self.request.user.groups.filter(name='moderator_group').exists():
            queryset = queryset.filter(owner=self.request.user).all()

        return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [EducationItemAccess]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [EducationItemAccess]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if not self.request.user.groups.filter(name='moderator_group').exists():
            queryset = queryset.filter(owner=self.request.user).all()

        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [EducationItemAccess]
