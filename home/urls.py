from django.urls import path 
from .views import *


urlpatterns = [
   
    path('',index, name= 'homepage'),
    path('store-location/', user_location , name='store-location')
]