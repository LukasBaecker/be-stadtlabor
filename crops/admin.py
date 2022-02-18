from django.contrib import admin

from .models import Crop

admin.site.register(Crop)
class CropAdmin(admin.ModelAdmin):
 list_display = ['crop_id','name','description','characteristics','image']
 
