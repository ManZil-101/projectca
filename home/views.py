from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserLocation
from home.models import IncidentInfo, Incidentlocation
from home.forms import IncidentForm
# Create your views here.
import math
import overpass.overpass as osm
 
import json
from django.core.serializers import serialize
@login_required()
def index(request):
    
    
    alert_location = list(Incidentlocation.objects.values())
    form1 = IncidentForm()
   
    context = {
        'alert_location':alert_location,
        'form1':form1
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
    

def show_alert(request, id):
    alert_location = list(Incidentlocation.objects.values())
    incident = IncidentInfo.objects.get(id=id)
    exact_location = Incidentlocation.objects.get(incident=incident)
    
    query_list=[]
    radius = str(10000)
    query_list.append(radius)
    query_list.append(str(exact_location.latitude))
    query_list.append(str(exact_location.longitude))
    print(query_list)

    
    query = (osm.get_hospital_query(query_list))
    data_frame = osm.extract_nodes_data_from_OSM(query)
    json_data = osm.extract_raw_data_from_OSM(query)





        
    names = []
    latitudes = []
    longitudes = []

    for element in json_data["elements"]:
        # if len(names) >= 4:  # Break the loop after 4 data points
        #     break
        if "tags" in element and "name" in element["tags"]:
            name = element["tags"]["name"]
            latitude = element["lat"]
            longitude = element["lon"]
            names.append(name)
            latitudes.append(latitude)
            longitudes.append(longitude)

    # Print the extracted information
    # for name, latitude, longitude in zip(names, latitudes, longitudes):
    #     print("Name:", name)
    #     print("Latitude:", latitude)
    #     print("Longitude:", longitude)
    #     print()



    # Function to calculate the distance between two sets of latitude and longitude
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in kilometers

        # Convert latitude and longitude to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c

        return distance

    # Desired location coordinates
    desired_latitude = exact_location.latitude
    desired_longitude = exact_location.longitude 

    # Find the nearest hospital
    nearest_hospital_index = None
    nearest_distance = float('inf')  # Set initial distance to infinity

    for i in range(len(names)):
        name = names[i]
        latitude = latitudes[i]
        longitude = longitudes[i]
        distance = calculate_distance(desired_latitude, desired_longitude, latitude, longitude)

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_hospital_index = i

    # Print the nearest hospital information
    if nearest_hospital_index is not None:
        nearest_hospital_name = names[nearest_hospital_index]
        nearest_hospital_latitude = latitudes[nearest_hospital_index]
        nearest_hospital_longitude = longitudes[nearest_hospital_index]

        print("Nearest Hospital:")
        print("Name:", nearest_hospital_name)
        print("Latitude:", nearest_hospital_latitude)
        print("Longitude:", nearest_hospital_longitude)
        print("Distance (in kilometers):", nearest_distance)
    else:
        print("No hospitals found.")
    
    nearest_hospital = {
        "Name": nearest_hospital_name,
        "Latitude": nearest_hospital_latitude,
        "Longitude": nearest_hospital_longitude,
        "Distance": nearest_distance

    }
    context = {
        'incident': incident,
        'nearest_hospital' :  nearest_hospital,
        'alert_location':alert_location
    }
    return render(request, 'home/show_alert.html', context)



