from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    users_with_access = models.ManyToManyField(User, through='ProductAccess', related_name='accessible_products')


    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product, related_name='lessons')


    def __str__(self):
        return self.name


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=20,
                              choices=[("Просмотрено", "Просмотрено"), ("Не просмотрено", "Не просмотрено")])

    def save(self, *args, **kwargs):
        # Проверяем, если просмотрено более 80% урока, устанавливаем статус "Просмотрено"
        if self.view_time_seconds >= 0.8 * self.lesson.duration_seconds:
            self.status = "Просмотрено"
        else:
            self.status = "Не просмотрено"
        super(LessonView, self).save(*args, **kwargs)
