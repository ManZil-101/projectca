from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserLocation
from home.models import IncidentInfo, Incidentlocation
# Create your views here.
import json
from django.core.serializers import serialize
@login_required()
def index(request):
   incidents = IncidentInfo.objects.get()
   alert_location = list(Incidentlocation.objects.values('latitude', 'longitude'))
   context = {
        
        'incidents': incidents,
    }
   return render(request, 'home/index.html', context)


def user_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        try:
            location = UserLocation.objects.get(user=request.user)
            location.latitude = latitude
            location.longitude = longitude
            location.save()
        except UserLocation.DoesNotExist:
            location = UserLocation.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude
            )
        
        return redirect('homepage')