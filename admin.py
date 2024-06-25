from django.contrib import admin
from .models import CustomUser, Product, Booking, Profile
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(Profile)