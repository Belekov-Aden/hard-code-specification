from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('api/all-lessons/', views.AllLessonsListAPIView.as_view(), name='lesson-list')
]
