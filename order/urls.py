from django.urls import path
from . import views

urlpatterns = [
        path('keranjang/', views.cart, name='keranjang'),
 path('tambah_cart/<int:product_id>/', views.tambah_cart, name='tambah_cart'),
  path('hapus-item/<int:cart_item_id>/', views.hapus_item, name='hapus_item'),  # URL untuk menghapus item
  path('checkout/', views.checkout, name='checkout'),
 ]
