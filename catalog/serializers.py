from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product, Lesson, LessonView, ProductAccess


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class LessonSerializer(serializers.ModelSerializer):
    view_time_seconds = serializers.IntegerField()
    status = serializers.CharField()

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ['user', 'lesson', 'view_time_seconds', 'status', 'view_date']


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializers()
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_views = LessonViewSerializer(many=True, read_only=True, source='lessonview_set')

    class Meta:
        model = Product
        fields = '__all__'


class ProductAccessSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = '__all__'


class ProductStatsSerializer(serializers.ModelSerializer):
    total_lesson_views = serializers.IntegerField()
    total_view_time = serializers.IntegerField()
    total_users = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'total_lesson_views', 'total_view_time', 'total_users', 'purchase_percentage']
