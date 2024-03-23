from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RegisterData(models.Model):
    name        =   models.CharField(max_length=50)
    dob         =   models.DateField()
    age         =   models.IntegerField()
    address     =   models.TextField()
    phone_no    =   models.IntegerField()
    email       =   models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    