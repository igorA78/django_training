from rest_framework import serializers

from education.models import Course, Lesson
from education.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            URLValidator(fields=['title', 'description', 'video_url'])
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            URLValidator(fields=['title', 'description'])
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return obj.subscription_set.filter(user=request.user).exists()
        return False


