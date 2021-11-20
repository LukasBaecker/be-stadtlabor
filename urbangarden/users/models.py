from django.db import models
from gardens.models import Garden

# Create your models here.

#Author: Brian Pondi - 20/11/2021

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    is_logged_in = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    privilege = models.OneToOneField('Privilege', on_delete=models.PROTECT, null=False)
    garden = models.ForeignKey(Garden, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username
    
class Privilege(models.Model):
    privilege_id = models.AutoField(primary_key=True)
    PRIVILEGE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),)
    privilege_name = models.CharField(max_length=50, choices=PRIVILEGE_CHOICES, default="USER")
    privilege_description = models.CharField(max_length=200)

    def __str__(self):
        return self.privilege_name




