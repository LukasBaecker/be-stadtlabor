from django.db import models
from django.contrib.auth.models import AbstractUser


#Author: Brian Pondi - 20/11/2021

class User(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=False)
    phone = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    username = None
    garden = models.ManyToManyField('gardens.Garden', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    
class GardenMembership(models.Model):
    ROLE_CHOICE = (
        ('1', 'Admin'),
        ('2', 'Member'))
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    garden = models.ForeignKey('gardens.Garden', on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICE, default='2', max_length=10)


