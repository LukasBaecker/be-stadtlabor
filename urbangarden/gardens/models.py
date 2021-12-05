from django.contrib.gis.db import models
from crops.models import Crop


#Author: Javier Martin - 20/11/2021

class Garden(models.Model):
    garden_id = models.AutoField(primary_key=True)
    longitude = models.FloatField(max_length=255, null=False)
    latitude = models.FloatField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1000)
    email = models.EmailField(max_length=255, unique=True, null=False)
    phone = models.CharField(max_length=255)
    crops= models.ManyToManyField(Crop)
    address = models.CharField(max_length=255, null = True)
    #geom_point =models.PointField(blank=True, null=True)
    #geom_polygon = models.PolygonField(blank=True, null=True)
    PURPOSE_CHOICES = (
        ("GARDEN", "Garden"),
        ("RESOURCES", "Resources"))
    primary_purpose =  models.CharField(max_length=255, choices=PURPOSE_CHOICES, default="RESOURCES")
    members = models.ManyToManyField('users.User', through='users.GardenMembership', related_name='gardens')

    def __str__(self):
        return self.name
    

class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    STATUS_CHOICES = (
        ("AVAILABLE FOR BORROWING", "Available for borrowing"),
        ("BORROWED", "Borrowed"),
        ("AVAILABLE FOR DONATION", "Available for donation"))
    resource_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="AVAILABLE")
    resource_name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null = True) 
    garden = models.ForeignKey('Garden',on_delete=models.PROTECT,null=False)
    #lender = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    #borrower = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, blank=True, null=True, related_name="%(user)s_related")

    def __str__(self):
        return self.resource_name

 #Author: Brian Pondi, Javier Martin and Nivedita Vee
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    CATEGORY_CHOICES=(("TOOLS",'Tools'),
                       ("SEEDS",'Seeds'),
                       ("FERTILIZERS",'Fertilizers'),
                       ("COMPOST", 'Compost'),
                       ("CONSTRUCTION_MATERIALS",'Construction_materials'),
                       ("GARDENS",'Gardens'),
                       ("OTHERS",'Others'))
    category_name = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="TOOLS")

    def __str__(self):
        return self.category_name






