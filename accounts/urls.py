from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.ProfileView, name='profile'),
    path('address/', views.AddressView, name= 'address'),
    path('store/', views.add_store, name= 'store'),
    path('sign/', views.SignView, name='sign'),
    path('signout/', views.SignOutView, name='signout'),
    path('signup/', views.SignUpView, name='signup'),
    path('seller/verification/', views.seller_verification, name='seller_verification'),
]
