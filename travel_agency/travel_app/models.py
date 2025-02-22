from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    guests = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=50)
    flights = models.CharField(max_length=50)
    budget = models.CharField(max_length=50)
    hotel_category = models.CharField(max_length=50)
    themes = models.TextField()  # Store multiple themes as a comma-separated string
    package_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.destination}"
