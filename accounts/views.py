from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings 
from accounts.form import *
from django.contrib.auth.decorators import login_required
from home.models import IncidentInfo, Incidentlocation
from home.forms import IncidentForm
# Create your views here.

def login_page(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username= username)
        
        if not user_obj.exists():
           
            messages.warning(request, "User Doesn't Exits")
            return HttpResponseRedirect(request.path_info)
        

        if not user_obj[0].profiles.is_email_varified:
            messages.warning(request, "Please Verify your email")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = username, password=password)
        if user_obj:
            login(request, user_obj)
            
            next_url = request.GET.get('next')

            if next_url is None:
                return redirect('dashboard')
            else:
                return redirect(next_url)
        else:
        
            messages.warning(request, "Invalid credentials")
            return HttpResponseRedirect(request.path_info)    
   



def register_page(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
        profile_form = ProfileForm()

        context = {
        'user_form': user_form,
        'profile_form': profile_form
        }

        return render(request, 'accounts/register.html', context)
    else:
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # username= request.POST.get('username')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # phone_number = request.POST.get('phonenumber')
        # address=request.POST.get('address')
        # citzenship_no=request.POST.get('citizenship')
        # citzenship_image=request.POST.get('citzenship_image')

        # user_obj = User.objects.filter(username= username)
        # user_obj1 = User.objects.filter(email=email)

        # if (user_obj.exists() or user_obj1.exists()):
        #     if user_obj1[0].email == email:
        #         messages.warning(request, "Email Already taken")
        #     else:
        #          messages.warning(request, "Username Already taken")
        #     return HttpResponseRedirect(request.path_info)

        # user_obj = User.objects.create(first_name = first_name, last_name=last_name, 
        #                                email=email, username=username)
        # user_obj.set_password(password)
        # user_obj.save()
        
        # profile = Profile.objects.get(user = user_obj)
       
        # profile.phone_number = phone_number
        # profile.address = address
        # profile.citzenship_no = citzenship_no
        # profile.citzenship_image =citzenship_image
        # profile.save()
         
    
        # messages.success(request, "Email has been sent to your mail.")
        # return HttpResponseRedirect(request.path_info)            
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
        
             # Save the user object

            # Associate the user with the profile
            phone_number = profile_form.cleaned_data['phone_number']
            address = profile_form.cleaned_data['address']
            citzenship_no = profile_form.cleaned_data['citzenship_no']
            citzenship_image = request.FILES.get('citzenship_image')

            profile = Profile.objects.get(user = user)
       
            profile.phone_number = phone_number
            profile.address = address
            profile.citzenship_no = citzenship_no
            profile.citzenship_image =citzenship_image
            profile.save()
            # Redirect or display a success message
            
            messages.success(request, "Email has been sent to your mail.")
            return HttpResponseRedirect(request.path_info)  
   

        else:
           
            messages.error(request, "error occur!!! Please resumbmit the form")
            print(profile_form.errors)
        
    


def activate_email(request, email_token):
    try:
        obj = Profile.objects.get(email_token=email_token)
        obj.is_email_varified = True
        obj.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("invailed email token")
    










# Create your views here.
@login_required()

def dashboard(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    try:
        incident = IncidentInfo.objects.get(user=user)
    except IncidentInfo.DoesNotExist:
        incident =None
    try:
        bloodinfo = Bloodinfo.objects.get(user=user)
    except Bloodinfo.DoesNotExist:
        bloodinfo = None
    
    if bloodinfo and incident:
        context = {
            'user': user,
            'profile': profile,
            'bloodinfo': bloodinfo,
            'incident':incident
        }
        return render(request, 'accounts/dashboard.html', context)
    elif not bloodinfo:
        if request.method == 'POST':
            form = BloodinfoForm(request.POST)
            if form.is_valid():
                bloodinfo = form.save(commit=False)
                bloodinfo.user = request.user
                bloodinfo.save()
                messages.success(request, "Blood information saved successfully.")
                return redirect('dashboard')
        else:
            form = BloodinfoForm()
        
        context = {
            'user': user,
            'profile': profile,
            'form': form,
        }
        return render(request, 'accounts/dashboard.html', context)
    else:
        alertform = IncidentForm()
        context = {
            'user': user,
            'profile': profile,
            'bloodinfo': bloodinfo,
            'form1':alertform
            
        }
        return render(request, 'accounts/dashboard.html', context)


@login_required()

def editblood(request, id):
    
    form = BloodinfoForm(request.POST)
    if request.method == 'GET':

        return render(request, 'accounts/bloodedit.html', context={'form':form})
    else:
        
        blood_group = form['blood_group']
        blood_donation_status = form['blood_donation_status']
        no_of_times = form['no_of_times']
        last_blood_donated = form['last_blood_donated']

        bloodinfo = Bloodinfo.objects.get(user = request.user)
        bloodinfo.blood_group = blood_group
        bloodinfo.blood_donation_status = blood_donation_status
        bloodinfo.no_of_times = no_of_times
        bloodinfo.last_blood_donated = last_blood_donated
        bloodinfo.save()
        #messages.success(request,"Profile updated")
        return redirect('dashboard')


@login_required()
def create_alert(request):
    
    location = UserLocation.objects.get(user = request.user)
    print(location.latitude)
    
    if request.method == 'POST':
        form=IncidentForm(request.POST or request.FILES )
        if  form.is_valid():
            incidents = form.save(commit=False)
            photo = request.FILES.get('photo')
            incidents.photo = photo
            incidents.user = request.user
            incidents.save()
            Incidentlocation.objects.create(
                incident = incidents,
                latitude = location.latitude,
                longitude = location.longitude

            )
            return redirect('dashboard')
            
            

   
