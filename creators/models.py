from django.db import models
from django.contrib.auth.models import User


class Creator(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, verbose_name='Phone number')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='creators', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
