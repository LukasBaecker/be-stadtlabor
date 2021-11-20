from django.db import models
from crops.models import Crop

# Create your models here.

#Author: Javier Martin - 20/11/2021

class Garden(models.Model):

    garden_id = models.AutoField(primary_key=True)
    longitude = models.FloatField(max_length=10, null=False)
    latitude = models.FloatField(max_length=10, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=400)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone = models.CharField(max_length=20)
    crops= models.ManyToManyField(Crop)
    #event = models.OneToMany('Event', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
    

class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ("AVAILABLE", "Available"),
        ("BORROWED", "Borrowed"),
        ("GIVEN", "Given"))
    resource_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="AVAILABLE")
    resource_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
    garden = models.ForeignKey(Garden,on_delete=models.PROTECT,null=False)

    def __str__(self):
        return self.resource_name

 #Author: Brian Pondi, Javier Martin and Nivedita Vee
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    CATEGORY_CHOICES=(("TOOLS",'Tools'),
                       ("SEEDS",'Seeds',
                       ("FERTILIZERS",'Fertilizers'),
                       ("CONSTRUCTION_MATERIALS",'Construction_materials'),
                       ("GARDENS",'Gardens'))               )
    category_name = models.CharField(max_length=100)


    def __str__(self):
        return self.category_name






