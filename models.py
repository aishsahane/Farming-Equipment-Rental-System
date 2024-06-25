# models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser , User
from django.db import models

from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    place = models.CharField(max_length=100)

    # Specify custom related names for groups and permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='user',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

CATEGORY_CHOICES = [
        ('tractors', 'Tractors'),
        ('tillage', 'Tillage Equipments'),
        ('seeding', 'Seeding Equipments'),
        ('landscape', 'Landscape Equipment'),
        ('crop_protection', 'Crop Protection'),
        ('harvest', 'Harvest Equipments'),
        ('post_harvest', 'Post Harvest'),
        ('haulage', 'Haulage'),
    ]

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES , default='tractors')
    description = models.TextField()
    manufacturer = models.TextField()
    equipment_location = models.CharField(max_length=200)
    daily_rental = models.IntegerField(default=0)
    hourly_rental = models.IntegerField(default=0)
    available_start_time = models.DateField()
    available_end_time = models.DateField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    QR_image = models.ImageField(upload_to='QR_images/', null=True, blank=True)

    def __str__(self):
        return self.name



class Booking(models.Model):
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'
    TIME_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)
    rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 

    def __str__(self):
        return f'{self.name} - {self.product}'
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_products = models.ManyToManyField(Product, related_name='added_by')
    bookings = models.ManyToManyField('Booking', blank=True, related_name='profile_bookings')

    def __str__(self):
        return f'{self.user} - {self.added_products} - {self.bookings}'
