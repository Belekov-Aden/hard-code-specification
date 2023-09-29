from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product, Lesson, LessonView, ProductAccess


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class LessonSerializer(serializers.ModelSerializer):
    view_time_seconds = serializers.IntegerField() # total_view_time
    status = serializers.CharField()
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = '__all__'


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
