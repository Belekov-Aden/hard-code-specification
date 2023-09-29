from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from django.db.models import Sum, F, Case, When, Value, IntegerField
from django.db import models

from .models import Product, ProductAccess, Lesson, LessonView
from .serializers import ProductSerializer, LessonSerializer


class AllLessonsListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     # Получаем список всех уроков с информацией о статусе и времени просмотра
    #     queryset = Lesson.objects.annotate(
    #         total_view_time=Sum(
    #             Case(
    #                 When(lessonview__user=user, lessonview__view_time_seconds__gt=F('duration_seconds') * 0.8,
    #                      then=F('duration_seconds')),
    #                 default=Value(0),
    #                 output_field=IntegerField(),
    #             )
    #         ),
    #         status=Case(
    #             When(total_view_time__gt=0, then=Value("Просмотрено")),
    #             default=Value("Не просмотрено"),
    #             output_field=models.CharField(),
    #         ),
    #     ).filter(products__users_with_access=user).distinct()
    #
    #     return queryset


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
