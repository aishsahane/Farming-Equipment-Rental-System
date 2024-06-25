# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Product , Booking

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=15)
    place = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'place', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','description','manufacturer', 'equipment_location','daily_rental','hourly_rental','available_start_time','available_end_time' ,'image']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['product', 'name', 'email', 'mobile_no', 'address', 'pincode', 'time','rent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget = forms.Select(choices=Booking.TIME_CHOICES)


class CategorySearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', 'All'),  # Add an option to select all categories
        ('tractors', 'Tractors'),
        ('tillage', 'Tillage Equipments'),
        ('seeding', 'Seeding Equipments'),
        ('landscape', 'Landscape Equipment'),
        ('crop_protection', 'Crop Protection'),
        ('harvest', 'Harvest Equipments'),
        ('post_harvest', 'Post Harvest'),
        ('haulage', 'Haulage'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)