from rest_framework import serializers

from .models import Product, ProductAccess, Lesson, LessonView
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', )

class ProductSerializers(serializers.ModelSerializer):
    owner = UserSerializers()

    class Meta:
        model = Product
        fields = '__all__'


class LessonSerializers(serializers.ModelSerializer):
    products = ProductSerializers(many=True)

    class Meta:
        model = Lesson
        fields = '__all__'