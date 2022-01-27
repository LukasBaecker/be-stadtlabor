from xml.dom.pulldom import default_bufsize
from django.db import models


#Author: Nivedita Vee - 20/11/2021

class Crop(models.Model):
    crop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    characteristics = models.TextField(max_length=500)
    image = models.ImageField(upload_to='images/')
    gardens=models.ManyToManyField('gardens.Garden')
    def __str__(self):
        return self.name

    





