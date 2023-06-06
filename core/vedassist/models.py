from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medicine(models.Model):

    user =models.ForeignKey(User , on_delete=models.SET_NULL , null=True,blank=True)
    medicine_name = models.CharField(max_length=100)
    medicine_price = models.FloatField(default=10.00)
    medicine_description= models.TextField(default="Default description")
    medicine_image = models.ImageField(upload_to = "medicine")
    medicine_view_count=models.IntegerField(default=1)

