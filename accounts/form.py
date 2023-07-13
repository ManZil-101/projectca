from django import forms
from django.contrib.auth.models import User
from accounts.models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'citzenship_no', 'citzenship_image')
        widgets = {
            'citzenship_image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        # required = {'citzenship_image': False}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control','placeholder': field.label})







class BloodinfoForm(forms.ModelForm):
    blood_group = forms.TypedChoiceField(
        choices=Bloodinfo.blood_group_type.choices,
        coerce=str,
        empty_value='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    blood_donation_status = forms.TypedChoiceField(
        choices=Bloodinfo.blood_donation_type.choices,
        coerce=str,
        empty_value='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    last_blood_donated = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Bloodinfo
        fields = ('blood_group', 'blood_donation_status', 'no_of_times', 'last_blood_donated')
