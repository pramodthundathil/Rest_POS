from django import forms
from .models import RestaurantDetails

class RestaurantDetailsForm(forms.ModelForm):
    class Meta:
        model = RestaurantDetails
        fields = [
            'Name_of_restaurant',
            'TRN',
            'location',
            'Address',
            'logo',
        ]
        widgets = {
            'Name_of_restaurant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Restaurant Name'}),
            'TRN': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter TRN'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'Address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
