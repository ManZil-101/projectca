from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserLocation, Profile
# Create your models here.

class IncidentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='incident_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    alert_status_type= models.TextChoices("alert_status_type", "Active Closed")
    alert_status = models.CharField(blank=True, choices=alert_status_type.choices, max_length=10, default= "Active" )
    def __str__(self):
        return self.incident_type
     



class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()



class PoliceStation(models.Model):
    station_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()



class Incidentlocation(models.Model):
    incident = models.OneToOneField(IncidentInfo, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()