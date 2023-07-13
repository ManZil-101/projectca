from django.urls import path 
from .views import *


urlpatterns = [
   
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('dashboard/', dashboard, name ='dashboard' ),
    path('activate/<email_token>', activate_email, name='activate_email'),
    path('edit/<id>', editblood, name='edit_blood'),
    path('create/', create_alert, name='create_alert' )
    
]

