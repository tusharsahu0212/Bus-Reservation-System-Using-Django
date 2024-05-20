from django.db import models

# Create your models here.

class Bus(models.Model):
    bus_name = models.CharField(max_length=20)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    nos = models.IntegerField()
    booked = models.IntegerField(default=0)
    price = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    

class Booking(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUS = [
        (BOOKED, "booked"),
        (CANCELLED, "cancelled"),
    ]

    user_id = models.IntegerField()
    bus_id = models.IntegerField()
    status = models.CharField(max_length=1, choices=TICKET_STATUS, default=BOOKED)
    nos = models.IntegerField()