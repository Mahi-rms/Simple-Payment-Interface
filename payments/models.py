from django.db import models
# Create your models here.
class Order(models.Model):
    payment_id=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    amount=models.FloatField()
    method=models.CharField(max_length=255,default="")