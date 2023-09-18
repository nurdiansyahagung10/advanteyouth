# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SellerVerification,UserAddress,Store

admin.site.register(CustomUser)
admin.site.register(UserAddress)
admin.site.register(SellerVerification)
admin.site.register(Store)