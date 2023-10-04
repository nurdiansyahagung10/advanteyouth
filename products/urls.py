from django.urls import path
from . import views

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('detailbarang/<slug:slug>/', views.databarang, name='detailbarang'),
    path('products/<str:category>/', views.filtered_products, name='filtered_products'),
    # Mungkin Anda juga perlu menambahkan rute untuk menampilkan daftar produk, kategori, dan nilai.
]
