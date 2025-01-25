from django import forms
from .models import RestaurantDetails

class RestaurantDetailsForm(forms.ModelForm):
    class Meta:
        model = RestaurantDetails
        fields = [
            'Name_of_restaurant',
            'TRN',
            'location',
            "phone",
            "mobile",
            'Address',
            'logo',
        ]
        widgets = {
            'Name_of_restaurant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Restaurant Name'}),
            'TRN': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter TRN'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'Address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Tax, AddOns, FoodCategory, Menu, Tables

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['tax_name', 'tax_percentage']
        widgets = {
            'tax_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tax name'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter tax percentage'}),
        }

class AddOnsForm(forms.ModelForm):
    class Meta:
        model = AddOns
        fields = ['name', 'price', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter add-on name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FoodCategoryForm(forms.ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name', 'image', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = [
            'category', 'name', 'image', 'potion', 'diet', 'price', 'status',
            'stock', 'description', 'code', 'tax', 'tax_value'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter menu name'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'potion': forms.Select(attrs={'class': 'form-control'}),
            'diet': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique code'}),
            'tax': forms.Select(attrs={'class': 'form-control'}),
            'tax_value': forms.Select(attrs={'class': 'form-control'}),
        }

class TablesForm(forms.ModelForm):
    class Meta:
        model = Tables
        fields = ['Table_number', 'Number_of_Seats', 'status']
        widgets = {
            'Table_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter table number'}),
            'Number_of_Seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of seats'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
