from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import pre_save
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    gender_choices = (
        ('null', 'prefer not to say'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=50, choices=gender_choices, default='null')
    bio = models.TextField(null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    has_store = models.BooleanField(default=False)

    def has_address(self):
        return UserAddress.objects.filter(UserAddressId=self).exists()

    def __str__(self):
        return self.username



class Store(models.Model):
    store_id = models.AutoField(primary_key=True, unique=True)
    store_seller_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    store_image = models.ImageField(upload_to='store_images/', blank=True, null=True)
    PhoneNumber = models.IntegerField()
    email = models.EmailField()
    store_name = models.CharField(max_length=100)
    store_description = models.TextField(null=True)
    Province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    post_code = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    store_open = models.TimeField()
    store_closed = models.TimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.store_name)


@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            # If the user is a superuser, add them to the 'Admin' group
            group_name = 'Admin'
        else:
            # If neither condition is met, add them to the 'Buyer' group
            group_name = 'Buyer'

        try:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass

class SellerVerification(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('approved', 'Approved'),
    )
    verification_image = models.ImageField(upload_to='verification_photos/')
    verification_status = models.CharField(max_length=10, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    verification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verifikasi {self.user_id.username}"
    
    def approve_verification(self):
        self.verification_status = 'approved'
        self.user_id.is_seller = True
        self.user_id.save()
        self.save()
        try:
            seller_group = Group.objects.get(name='Seller')
            buyer_group = Group.objects.get(name='Buyer')
            self.user_id.groups.add(seller_group)
            self.user_id.groups.remove(buyer_group)
        except Group.DoesNotExist:
            pass

    def cancel_verification(self):
        self.verification_status = 'canceled'
        self.user_id.is_seller = False
        self.user_id.save()
        self.save()
        seller_group = Group.objects.get(name='Seller')
        buyer_group = Group.objects.get(name='Buyer')
        self.user_id.groups.remove(seller_group)
        self.user_id.groups.add(buyer_group)
        self.delete()  # Ini akan menghapus data verifikasi dari tabel

    
class UserAddress(models.Model):
    UserAddressId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    PhoneNumber = models.IntegerField()
    Province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    post_code = models.CharField(max_length=100)
    street = models.CharField(max_length=100, unique=True)
    detail = models.TextField(null=True)
    address_for = models.CharField(max_length=10, choices=[('kantor', 'Kantor'), ('rumah', 'Rumah')])    
    Main_address = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
    # Jika alamat ini akan menjadi alamat utama, maka set alamat utama lainnya ke False
        if self.Main_address:
            UserAddress.objects.filter(UserAddressId=self.UserAddressId).exclude(id=self.id).update(Main_address=False)
        super(UserAddress, self).save(*args, **kwargs)


    @property
    def full_name(self):
        custom_user = self.UserAddressId
        return f"{custom_user.first_name} {custom_user.last_name}"
    

@receiver(pre_save, sender=UserAddress)
def ensure_single_main_address(sender, instance, **kwargs):
    if instance.Main_address:
        # Set semua alamat utama user ini ke False sebelum menyimpan yang baru
        UserAddress.objects.filter(UserAddressId=instance.UserAddressId).exclude(id=instance.id).update(Main_address=False)
