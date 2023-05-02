from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.time_create}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-time_create',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time_create}, {self.post}"

    class Meta:
        ordering = ('-time_create',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

