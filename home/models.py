from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class UserInfo(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MaxValueValidator(100),
                                           MinValueValidator(1)])
    GENDER_TYPE = [
    ("male", "male"),
    ("female", "female"),
    ]
    gender = models.CharField(max_length=7, choices=GENDER_TYPE)
    email = models.CharField(max_length=50)
    password = models.TextField()
