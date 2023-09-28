from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('api/v1/product/', views.ProductAPIView.as_view()),
    path('api/v1/lesson/', views.LessonAPIView.as_view()),
]
