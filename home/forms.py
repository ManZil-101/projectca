from django import forms

from home.models import *

class IncidentForm(forms.ModelForm):
   

    class Meta:
        model = IncidentInfo
        fields = ('incident_type','description','alert_status','photo')


        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control-file'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})
