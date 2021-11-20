from django.db import models
from gardens.models import Garden
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

#Author: Brian Pondi - 20/11/2021

class User(AbstractBaseUser):
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
    privilege = models.OneToOneField('Privilege', on_delete=models.PROTECT, null=False)
    garden = models.ForeignKey(Garden, on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    
class Privilege(models.Model):
    privilege_id = models.AutoField(primary_key=True)
    PRIVILEGE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),)
    privilege_name = models.CharField(max_length=50, choices=PRIVILEGE_CHOICES, default="USER")
    privilege_description = models.CharField(max_length=200)

    def __str__(self):
        return self.privilege_name




