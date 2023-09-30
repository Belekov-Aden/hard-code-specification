from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('api/all-lessons/', views.AllLessonsListAPIView.as_view(), name='lesson-list'),
    path('api/detail-lessons/<int:product_id>/', views.DetailLessonViewsListAPIView.as_view(), name='lesson-detail'),
    path('api/stats-products/', views.ProductStatsAPIView.as_view(), name='product-stats'),
]
