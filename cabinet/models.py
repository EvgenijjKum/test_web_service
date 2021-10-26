from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    age = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    STATUS = (
        ('renter', 'Renter'),
        ('owner', 'Owner'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='renter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return f'{self.username}, {self.first_name}, {self.last_name}'
