from django.db import models
from gardens.models import Garden
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

#Author: Brian Pondi - 20/11/2021

class User(models.Model):
    user_id = models.AutoField(primary_key=True, editable=False)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, null=False)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    is_logged_in = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    #garden = models.ManyToManyField(Garden, on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class GardenMembership(models.Model):
    ROLE_CHOICE = (
        ('1', 'Admin'),
        ('2', 'Member'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICE, default='2', max_length=1)


