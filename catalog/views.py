from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from django.db import models
from django.db.models import Count, Sum, F

from .models import Product, ProductAccess, Lesson, LessonView, User
from .serializers import ProductSerializer, LessonSerializer, LessonViewSerializer, \
ProductStatsSerializer



class AllLessonsListAPIView(generics.ListAPIView):
    '''
    Все уроки по всем продуктам к которым пользователь имеет доступ.
    Также с выведением о статусе и времени просмотра.
    '''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lessons = Lesson.objects.filter(products__users_with_access=user)

        result = []

        for lesson in lessons:
            try:
                lesson_view = LessonView.objects.get(user=user, lesson=lesson)
                lesson.status = lesson_view.status
                lesson.view_time_seconds = lesson_view.view_time_seconds
            except LessonView.DoesNotExist:
                # Если у пользователя нет информации о просмотре урока, устанавливаем статус "Не просмотрено"
                lesson.status = "Не просмотрено"
                lesson.view_time_seconds = 0

            # Добавляем урок в список
            result.append(lesson)

        return result


class DetailLessonViewsListAPIView(generics.ListAPIView):
    '''
    Список уроков по конкретному продукту (product_id) к которому пользователь имеет доступ.
    Также с выводом о статусе, времени просмотра дата последнего просмотра ролика.
    '''
    serializer_class = LessonViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        if not Product.objects.filter(id=product_id, users_with_access=user).exists():
            return LessonView.objects.none()

        queryset = LessonView.objects.filter(user=user, lesson__products=product_id).select_related('lesson')
        return queryset


class ProductStatsAPIView(generics.ListAPIView):
    '''
    Статистика по продуктам:
        - Количество просмотренных уроков от всех учеников.
        - Сколько в сумме все ученики потратили времени на просмотр роликов.
        - Количество учеников занимающихся на продукте.
        - Процент приобретения продукта (рассчитывается исходя из количества полученных доступов
        к продукту деленное на общее количество пользователей на платформе
    '''
    serializer_class = ProductStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        queryset  = Product.objects.annotate(
            total_lesson_views=Sum('lessons__lessonview__view_time_seconds'),
            total_view_time=Sum('lessons__lessonview__view_time_seconds'),
            total_users=Count('productaccess__user'),
            total_accesses=Count('productaccess'),
            purchase_percentage=(Count('productaccess__user') / F('total_users')) * 100
        ).order_by('id')

        return queryset