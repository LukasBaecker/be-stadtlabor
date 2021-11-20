from django.db import models

# Create your models here.

#Author: Nivedita Vee - 20/11/2021

class Crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    characteristics = models.TextField(max_length=500)
    image = models.ImageField()
   
    # garden = models.ForeignKey('Garden', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
    





