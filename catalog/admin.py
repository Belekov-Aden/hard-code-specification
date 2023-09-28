from django.contrib import admin

from . import models

@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_link', 'duration_seconds')
    list_filter = ('name', 'duration_seconds')
    search_fields = ('name', 'video_link')


@admin.register(models.LessonView)
class LessonViewAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'view_time_seconds', 'status')
    list_filter = ('lesson', 'view_time_seconds', 'status')
    search_fields = ('lesson', 'status')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name',)


@admin.register(models.ProductAccess)
class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user', 'product')