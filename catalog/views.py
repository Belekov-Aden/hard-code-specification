from django.shortcuts import render

from rest_framework import generics
from rest_framework.generics import GenericAPIView

from . import models as catalog_models
from .serializers import ProductSerializers, LessonSerializers


class ProductAPIView(generics.ListAPIView):
    queryset = catalog_models.Product.objects.all()
    serializer_class = ProductSerializers


class LessonAPIView(generics.ListAPIView):
    queryset = catalog_models.Lesson.objects.all()
    serializer_class = LessonSerializers


class LessonsInProductWhere:
    pass