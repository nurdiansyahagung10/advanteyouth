from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('order_history/', views.order_history, name='order_history'),
    path('replace_order/<int:item_id>/', views.replace_order, name='replace_order'),

]
