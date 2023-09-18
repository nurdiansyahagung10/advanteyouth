from django.urls import path
from . import views 

urlpatterns = [
    path('seller/verification_list/<int:pk>/approve/', views.approve_verification, name='approve_verification'),
    path('seller/verification_list/<int:pk>/cancel/', views.cancel_verification, name='cancel_verification'),
    path('seller/verification_list/', views.verification_list, name='verification_list'),
     path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
]
