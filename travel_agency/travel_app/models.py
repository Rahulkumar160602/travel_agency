from django.db import models
from djongo import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    guests = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

# Create your models here.


