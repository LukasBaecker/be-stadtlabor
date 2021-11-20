from django.db import models
from gardens.models import Garden

# Create your models here.

#Author: Nivedita Vee- 20/11/2021

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    venue = models.CharField(max_length=100)
    date= models.DateTimeField()
    duration = models.TimeField(null=False)
    garden = models.ForeignKey(Garden, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title
    




