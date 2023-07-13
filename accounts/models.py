from django.db import models
from base.model import BaseModel
from base.emails import send_account_activation_email
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    is_email_varified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    citzenship_no = models.CharField(max_length=50)
    citzenship_image = models.ImageField(upload_to = 'citizenship')

    
    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user= instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)







class UserLocation(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="userlocation")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)




class Bloodinfo(models.Model):
    blood_group_type= models.TextChoices("blood_group_type", "A+ A- B+ B- O+ O- AB+ AB-")
    blood_group = models.CharField(blank=True, choices=blood_group_type.choices, max_length=10 )

    blood_donation_type= models.TextChoices(" blood_donation_type", " Active Inactive")
    blood_donation_status = models.CharField(blank=True, choices= blood_donation_type.choices, max_length=10, default="Inactive" )

    no_of_times = models.IntegerField()
    last_blood_donated = models.DateField()

    user = models.OneToOneField(User, on_delete=models.CASCADE)




class BloodBank(models.Model):
    bloodbank_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.bloodbank_name
    
